project('GStreamer documentation', 'c', version: '1.15.0.1')

hotdoc = import('hotdoc')
hotdoc_subprojects = []
libs = ''
plugins_sitemap = ''

apiversion = '1.0'
if host_machine.system() == 'windows'
  pathsep = ';'
else
  pathsep = ':'
endif

message('Got projects: ' + get_option('built_subprojects'))
libs = ''
plugins_doc = ''
gst_plugins_path = ''
deps = []
if get_option('built_subprojects') != ''
    foreach project_name: get_option('built_subprojects').split(',')
        sub = subproject(project_name)
        if sub.get_variable('build_hotdoc')
            message('Building @0@ documentation'.format(project_name))

            foreach lib: sub.get_variable('libs_doc')
              hotdoc_subprojects += [lib]
              libs += lib.full_path() + pathsep
            endforeach

            foreach plugin_doc: sub.get_variable('plugins_doc')
              plugins_doc += plugin_doc.full_path() + pathsep
              hotdoc_subprojects += [plugin_doc]
            endforeach

            foreach plugin_path: sub.get_variable('all_plugins_paths')
              gst_plugins_path += plugin_path + pathsep
            endforeach
        else
            message('@0@ did not build hotdoc, can\'t build API doc'.format(project_name))
        endif
    endforeach
endif

if get_option('use_portal_index')
  index = 'markdown/index.md'
else
  index = 'markdown/simple-index.md'
endif
sitemap_gen = find_program('scripts/generate_sitemap.py')
sitemap = configure_file(command: [sitemap_gen, '@INPUT@', '@OUTPUT@',
  index.split('/')[1], libs, plugins_doc],
  input: 'sitemap.txt',
  output: 'sitemap.txt')

html_theme = 'https://github.com/hotdoc/hotdoc_lumen_theme/releases/download/0.6/hotdoc_lumen_theme-0.6.tar.xz?sha256=0e2f175f4cf8c00ed7ac5014e30c806a294b0d3818565eb74e1424a948e8a452'

gstreamer_doc = hotdoc.generate_doc('GStreamer',
    project_version: apiversion,
    sitemap: sitemap,
    index: index,
    install: true,
    extra_assets: [join_paths(meson.current_source_dir(), 'images')],
    syntax_highlighting_activate: true,
    html_theme: html_theme,
    include_paths: join_paths(meson.current_source_dir(), 'examples'),
    html_extra_theme: join_paths(meson.current_source_dir(), 'theme/extra'),
    dependencies: deps,
    subprojects: hotdoc_subprojects,
    disable_incremental_build: true,
    gst_list_plugins_page: 'plugins_doc.md',
    gst_plugins_path: gst_plugins_path,
    default_license: 'CC-BY-SAv4.0',
    devhelp_activate: true,
)