typedef struct _hexchat_plugin hexchat_plugin;

int on_command (char **word, char **word_eol, void *user_data);
int plugin_init (hexchat_plugin *ph);
int plugin_deinit (void);