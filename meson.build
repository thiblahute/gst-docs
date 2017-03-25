project('GStreamer manuals and tutorials', 'c', version: '1.11.1.1')

hotdoc = import('hotdoc')
hotdoc_subprojects = []
api_subprojs = ''

message('Got projects: ' + get_option('built_subprojects'))
if get_option('built_subprojects') != ''
    foreach project_name: get_option('built_subprojects').split(',')
        message('Getting ' + project_name)
        gst_sub = subproject(project_name)
        if gst_sub.get_variable('build_hotdoc')
            doc_variable = project_name.underscorify() + '_doc'
            doc_json = project_name + '-doc.json'
            hotdoc_subprojects += [gst_sub.get_variable(doc_variable)]
            api_subprojs += '\n	' + doc_json
            message('Building @0@ documentation'.format(project_name))
        else
            message('@0@ did not build hotdoc, can\'t build API doc'.format(project_name))
        endif
    endforeach
endif

gst_dep = dependency('gstreamer-1.0', fallback : ['gstreamer', 'gst_dep'])

if api_subprojs != ''
    api_subprojs = 'api.md' + api_subprojs
endif

sitemap_gen = find_program('generate_sitemap.py')
cmdres = run_command(sitemap_gen, api_subprojs)
if cmdres.returncode() != 0
    error('Generating sitemap failed @0@: @1@'.format(sitemap_gen,
        cmdres.stderr()))
endif

theme = subproject('hotdoc_bootstrap_theme',
        default_options: ['less_include_path=' +
            join_paths(meson.current_source_dir(), 'theme/less')]
        )

gstreamer_doc = hotdoc.generate_doc('GStreamer',
    project_version: '1.0',
    sitemap: 'generated_sitemap.txt',
    index: 'markdown/index.md',
    install: true,
    extra_assets: [join_paths(meson.current_source_dir(), 'images')],
    syntax_highlighting_activate: true,
    html_theme: theme.get_variable('theme_dir'),
    include_paths: join_paths(meson.current_source_dir(), 'examples'),
    html_extra_theme: join_paths(meson.current_source_dir(), 'theme/extra'),
    dependencies: [theme.get_variable('theme_dep')] + [gst_dep],
    subprojects: hotdoc_subprojects,
    disable_incremental_build: true,
    gst_list_all_plugins: true,
)
