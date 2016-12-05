# The gst-validate-transcoding command line tool

`gst-validate-transcoding` \[options...\] \[INPUT-URI\] \[OUTPUT-URI\]

## Description

**gst-validate-transcoding** is tool to create media files transcoding
pipelines running inside the GstValidate monitoring infrastructure.

You can for example transcode any media file to Vorbis audio + VP8 video
in a WebM container by doing:

```
gst-validate-transcoding-1.0 file:///./file.ogg file:///.../transcoded.webm -o video/webm:video/x-vp8:audio/x-vorbis
```

**gst-validate-transcoding** will list every issue encountered during
the execution of the transcoding operation in a human readable report
like the one below:

```
issue : buffer is out of the segment range Detected on
theoradec0.srcpad at 0:00:00.096556426 Details : buffer is out of
segment and shouldn't be pushed. Timestamp: 0:00:25.000 -
duration: 0:00:00.040 Range: 0:00:00.000 - 0:00:04.520 Description :
buffer being pushed is out of the current segment's start-stop range.
Meaning it is going to be discarded downstream without any use
```

The return code of the process will be 18 in case a `CRITICAL` issue has been found.

### The encoding profile serialization format

This is the serialization format of a
[GstEncodingProfile].

Internally the transcoding application uses [GstEncodeBin]
**gst-validate-transcoding-1.0** uses its own serialization format to describe the
[GstEncodeBin.profile] property of the encodebin.

The simplest serialized profile looks like:

    muxer_source_caps:videoencoder_source_caps:audioencoder_source_caps

For example to encode a stream into a WebM container, with an OGG audio
stream and a VP8 video stream, the serialized
[GstEncodingProfile] will look like:

    video/webm:video/x-vp8:audio/x-vorbis

You can also set the preset name of the encoding profile using the
caps+preset\_name syntax as in:

    video/webm:video/x-vp8+youtube-preset:audio/x-vorbis

Moreover, you can set the
[presence](https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gst-plugins-base-libs-1.0gst-plugins-base-libs-encoding-profile.html#gst-encoding-profile-set-presence)
property of an encoding profile using the `|presence` syntax as in:

    video/webm:video/x-vp8|1:audio/x-vorbis

This field allows you to specify how many times maximum a
[GstEncodingProfile](https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gst-plugins-base-libs-1.0gst-plugins-base-libs-encoding-profile.html#GstEncodingProfile-struct)
can be used inside an encodebin.

You can also use the `restriction_caps->encoded_format_caps` syntax to
specify the restriction caps to be set on a
[GstEncodingProfile](https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gst-plugins-base-libs-1.0gst-plugins-base-libs-encoding-profile.html#GstEncodingProfile-struct).
It corresponds to the restriction
[GstCaps] to apply before the encoder that will be used in the profile. The fields
present in restriction caps are properties of the raw stream (that is,
before encoding), such as height and width for video and depth and
sampling rate for audio. This property does not make sense for muxers.

To force a video stream to be encoded with a Full HD resolution (using
WebM as the container format, VP8 as the video codec and Vorbis as the
audio codec), you should use:

    video/webm:video/x-raw,width=1920,height=1080-&gt;video/x-vp8:audio/x-vorbis

#### Some serialized encoding formats examples:

#### MP3 audio and H264 in MP4:

    video/quicktime,variant=iso:video/x-h264:audio/mpeg,mpegversion=1,layer=3

#### Vorbis and theora in OGG:

    application/ogg:video/x-theora:audio/x-vorbis

#### AC3 and H264 in MPEG-TS:

    video/mpegts:video/x-h264:audio/x-ac3

## Invocation

**gst-validate-transcoding** takes an input URI and an output URI, plus
a few options to control how transcoding should be tested.

### Options

**`-o`**, -**`-output-format`**=properties-values     Set the properties to use
for the encoding profile (in case of transcoding.) For example:

**`--set-scenario`**: Let you set a scenario, it can be a full path to a
scenario file or the name of the scenario (name of the file without the
'.scenario' extension).

**`--set-configs`**: Let you set a config scenario, the scenario needs to be
set as 'config' you can specify a list of scenario separated by ':' it will
override the GST_VALIDATE_SCENARIO environment variable,

**`-e`**, **`--eos-on-shutdown`**: If an EOS event should be sent to the
pipeline if an interrupt is received, instead of forcing the pipeline to stop.
Sending an EOS will allow the transcoding to finish the files properly before
exiting.

**`-l`**, **`--list-scenarios`**: List the available scenarios that can be run

**`-t`**, **`--inspect-action-type`**: Inspect the available action types with
which to write scenarios if no parameter passed, it will list all available
action types otherwise will print the full description of the wanted types

**`--scenarios-defs-output-file`**: The output file to store scenarios details.
Implies --list-scenario

**`-r`**, **`--force-reencoding`**: Whether to try to force reencoding, meaning
trying to only remux if possible(default: TRUE)

[GstCaps]: https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gstreamer-1.0GstCaps.html#GstCaps-struct
[GstEncodingProfile]: https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gst-plugins-base-libs-1.0gst-plugins-base-libs-encoding-profile.html#GstEncodingProfile-struct
[GstEncodeBin]: https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gst-plugins-base-plugins-1.0gst-plugins-base-plugins-encodebin.html#GstEncodeBin-struct
[GstEncodeBin.profile]: https://gstreamer.freedesktop.org/usr/share/gtk-doc/html/gst-plugins-base-plugins-1.0gst-plugins-base-plugins-encodebin.html#GstEncodeBin--profile
