## Audiosink design

### Requirements

  - must operate chain based. Most simple playback pipelines will push
    audio from the decoders into the audio sink.

  - must operate getrange based Most professional audio applications
    will operate in a mode where the audio sink pulls samples from the
    pipeline. This is typically done in a callback from the audiosink
    requesting N samples. The callback is either scheduled from a thread
    or from an interrupt from the audio hardware device.

  - Exact sample accurate clocks. the audiosink must be able to provide
    a clock that is sample accurate even if samples are dropped or when
    discontinuities are found in the stream.

  - Exact timing of playback. The audiosink must be able to play samples
    at their exact times.

  - use DMA access when possible. When the hardware can do DMA we should
    use it. This should also work over bufferpools to avoid data copying
    to/from kernel space.

### Design

The design is based on a set of base classes and the concept of a
ringbuffer of samples.

    +-----------+   - provide preroll, rendering, timing
    + basesink  +   - caps nego
    +-----+-----+
          |
    +-----V----------+   - manages ringbuffer
    + audiobasesink  +   - manages scheduling (push/pull)
    +-----+----------+   - manages clock/query/seek
          |              - manages scheduling of samples in the ringbuffer
          |              - manages caps parsing
          |
    +-----V------+   - default ringbuffer implementation with a GThread
    + audiosink  +   - subclasses provide open/read/close methods
    +------------+

The ringbuffer is a contiguous piece of memory divided into segtotal
pieces of segments. Each segment has segsize bytes.

          play position 
            v          
    +---+---+---+-------------------------------------+----------+
    + 0 | 1 | 2 | ....                                | segtotal |
    +---+---+---+-------------------------------------+----------+
    <--->
      segsize bytes = N samples * bytes_per_sample.
  
The ringbuffer has a play position, which is expressed in segments. The
play position is where the device is currently reading samples from the
buffer.

The ringbuffer can be put to the PLAYING or STOPPED state.

In the STOPPED state no samples are played to the device and the play
pointer does not advance.

In the PLAYING state samples are written to the device and the
ringbuffer should call a configurable callback after each segment is
written to the device. In this state the play pointer is advanced after
each segment is written.

A write operation to the ringbuffer will put new samples in the
ringbuffer. If there is not enough space in the ringbuffer, the write
operation will block. The playback of the buffer never stops, even if
the buffer is empty. When the buffer is empty, silence is played by the
device.

The ringbuffer is implemented with lockfree atomic operations,
especially on the reading side so that low-latency operations are
possible.

Whenever new samples are to be put into the ringbuffer, the position of
the read pointer is taken. The required write position is taken and the
diff is made between the required and actual position. If the difference
is \<0, the sample is too late. If the difference is bigger than
segtotal, the writing part has to wait for the play pointer to advance.

### Scheduling

#### chain based mode

In chain based mode, bytes are written into the ringbuffer. This
operation will eventually block when the ringbuffer is filled.

When no samples arrive in time, the ringbuffer will play silence. Each
buffer that arrives will be placed into the ringbuffer at the correct
times. This means that dropping samples or inserting silence is done
automatically and very accurate and independend of the play pointer.

In this mode, the ringbuffer is usually kept as full as possible. When
using a small buffer (small segsize and segtotal), the latency for audio
to start from the sink to when it is played can be kept low but at least
one context switch has to be made between read and write.

#### getrange based mode

In getrange based mode, the audiobasesink will use the callback
function of the ringbuffer to get a segsize samples from the peer
element. These samples will then be placed in the ringbuffer at the
next play position. It is assumed that the getrange function returns
fast enough to fill the ringbuffer before the play pointer reaches
the write pointer.
    
In this mode, the ringbuffer is usually kept as empty as possible.
There is no context switch needed between the elements that create
the samples and the actual writing of the samples to the device.

#### DMA mode

Elements that can do DMA based access to the audio device have to
subclass from the GstAudioBaseSink class and wrap the DMA ringbuffer
in a subclass of GstRingBuffer.
    
The ringbuffer subclass should trigger a callback after writing or
playing each sample to the device. This callback can be triggered
from a thread or from a signal from the audio device.

### Clocks

The GstAudioBaseSink class will use the ringbuffer to act as a clock
provider. It can do this by using the play pointer and the delay to
calculate the clock time.
