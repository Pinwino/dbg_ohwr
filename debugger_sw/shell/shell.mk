# This work is part of the White Rabbit project
# 
# Jose Jimenez  <jjimenez.wr@gmail.com>, Copyright (C) 2014 UGR.
# 
#  Released according to the GNU GPL version 3 (GPLv3) or later.
# 

obj-y += \
	shell/shell.o \
	shell/cmd_sdb.o \
	shell/cmd_help.o \
	shell/cmd_sleep.o

obj-$(CONFIG_MEM_CHECK_CMD) += shell/cmd_dbgmem.o
