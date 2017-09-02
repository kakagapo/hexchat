#undef HAVE_STRINGS_H
#undef HAVE_MEMRCHR

#include "config.h"
#include "exports.h"
#include "hexchat-plugin.h"

int
hexchat_plugin_init(hexchat_plugin *plugin_handle,
                    char **plugin_name,
                    char **plugin_desc,
                    char **plugin_version,
                    char *arg)
{
	*plugin_name = "Python";
	*plugin_version = "1.0";
	*plugin_desc = "Python support";

	return plugin_init (plugin_handle);
}

int
hexchat_plugin_deinit(void)
{
	return plugin_deinit ();
}
