pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'adventure'
gnome = import('gnome')

gnome.compile_resources('adventure',
  'adventure.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'adventure.in',
  output: 'adventure',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)
configure_file(
  input: 'adventure-cli.in',
  output: 'adventure-cli',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

adventure_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'actions.py',
  'parser.py',
  'cli.py',
  'style.css',
]

install_data(adventure_sources, install_dir: moduledir)
