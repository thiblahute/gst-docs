---
title: GStreamer tester guide
short-description: Complete walkthrough for running and creating tests for GStreamer
...

# GStreamer tester guide

These guide describe the testing frameworks, tools and infrastructure used
to test the GStreamer framework.

There are mainly two complementary types of tests which have different purposes:

 * Unit tests, those are available in the different GStreamer modules under the
 `tests/check/XXX` directories. Those tests are based on the [libcheck] unit
 testing framework and the gstcheck library. They aim at checking each part of
 code behaviour independently.

 * [Integration tests](testing/integration-tests.md), those are based
 on the [GstValidate] integration testing framework for GStreamer. They test how
 things behave at a higher level running actual pipeline, with media files, with
 different protocols etc.. The official integration testsuites, with the
 associated media assets are available in the [gst-integration-testsuites]
 module.

[libcheck]: https://libcheck.github.io/check/
[gstvalidate]: https://cgit.freedesktop.org/gstreamer/gst-devtools/tree/validate
[gst-integration-testsuites]: https://cgit.freedesktop.org/gstreamer/gst-integration-testsuites
