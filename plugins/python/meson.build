python_opt = get_option('with-python')
python_dep = dependency(python_opt, version: '>= 3.3')

python3_source = custom_target('python-bindings',
  input: ['exports.h', 'imports.h', 'init.c', 'init.py'],
  output: 'python.c',
  command: [find_program('generate_plugin.py'), '@INPUT@', '@OUTPUT@']
)

install_data('hexchat.py', install_dir: plugindir)

shared_module('python', python3_source,
  dependencies: [hexchat_plugin_dep, python_dep],
  install: true,
  install_dir: plugindir,
  name_prefix: '',
)
