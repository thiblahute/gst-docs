# GStreamer validate integration framework

GstValidate is an integration framework that allows GStreamer developers to
check that the GstElements they write behave the way they are supposed to. It
was first started to provide plug-ins developers with a tool to check that they
use the framework the proper way and since then has been extended to provide
a full integration testsuite framework for developers that using and working on
GStreamer.

## Pipeline monitoring

GstValidate implements a monitoring logic that allows the framework to check
that the elements of a GstPipeline respect some rules GStreamer components have
to follow to make them properly interact together. For example, every pad in
a GStreame pipeline will is wrapped by a GstValidatePadMonitor which will make
sure that if we receive a GstSegment from upstream, an equivalent segment is
sent downstream before any buffer gets out.

GstValidate is implemented as a GStreamer [tracer](design/tracing.md) which means
that the monitoring system can be activated on any application using GStreamer setting
the `GST_TRACERS` environment variable as follow:

```
GST_TRACERS=validate my-gstreamer-app
```

## GstValidate issue reporting system

Then GstValidate implements a reporting system that allows users to get
detailed informations about what issues happened. It tries to gather as much
information as possible so the user can more easily understand and fix
issues. The generated reports are ordered by level of importance from
"issue" to "critical".

## command line tools

The GStreamer validation framework comes with a set of command line tools to validate
and test pipelines and use cases as simply as possible:

  * [gst-validate] : [gst-launch](tools/gst-launch.md) like tool to run GStreamer
    pipelines under the GstValidate watch.
  * [gst-validate-transcoding]: Tool allowing to simply transcode media files from
    one media format to another.
  * [gst-validate-media-check]: A tool to verify GStreamer media analysis results (trough
    the #GstDiscoverer API and some extensions)

## GstValidate scenarios

On top of that, the notion of a [scenario](#scenarios) has
been implemented so that developers can easily execute a set of actions
on pipelines to test real world interactive cases and reproduce existing
issues in a convenient way.

## Run the default testsuite

You can simply setup and run the GStreamer default testsuite using the
[gst-validate-launcher] tool:

``` bash
# the `--sync` option is needed so to setup the testsuite and download the default media files
gst-validate-launcher --sync
```

> NOTES:
> - The testsuites are downloaded in your home folder under `gst-validate/`, that can be changed with the `--main-dir` option)
> - You will need `git` and [git annex] available in your `PATH` to download the testsuite

[gst-validate]: testing/gst-validate.md
[gst-validate-transcoding]: testing/gst-validate-transcoding.md
[gst-validate-media-check]: testing/gst-validate-media-check.md
[gst-validate-launcher]: FIXME!
[git annex]: https://git-annex.branchable.com/
