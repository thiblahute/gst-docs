project('GStreamer manuals and tutorials', 'c', version: '1.11.1.1')

hotdoc = import('hotdoc')
hotdoc_subprojects = []
api_subprojs = ''
if get_option('gstreamer_core_api')
    gst_sub = subproject('gstreamer')

    if gst_sub.get_variable('build_gir')
        hotdoc_subprojects += [gst_sub.get_variable('gstreamer_doc')]
        api_subprojs += '\n		gstreamer-doc.json'
        message('Building GStreamer core API documentation')
    else
        message('GStreamer core did not build the GIR, can\'t build API doc')
    endif
else
    message('NOT building GStreamer core API documentation')
endif

if api_subprojs != ''
    api_subprojs = '	api.md' + api_subprojs
endif

python3 = find_program('python3')
sitemap_generator = '''
with open('@0@/sitemap.txt.in') as f:
    with open('@0@/sitemap.txt', 'w') as fw:
        fw.write(f.read() % {'api': """@1@"""})
'''.format(meson.current_source_dir(), api_subprojs)

cmdres = run_command(python3, '-c', sitemap_generator)
if cmdres.returncode() != 0
    error('Generating sitemap failed @0@: @1@'.format(sitemap_generator,
        cmdres.stderr()))
endif

gstreamer_doc = hotdoc.generate_doc('GStreamer',
    project_version: '1.0',
    sitemap: 'sitemap.txt',
    index: 'markdown/index.md',
    install: true,
    dependencies: hotdoc_subprojects
)
