# This work is part of the White Rabbit project
# 
# Jose Jimenez  <jjimenez.wr@gmail.com>, Copyright (C) 2014 UGR.
# 
# Released according to the GNU GPL version 3 (GPLv3) or later.
# 

obj-y += $(WRPC_DIR)/pp_printf/printf.o

ppprintf-$(CONFIG_PRINTF_FULL) += $(WRPC_DIR)/pp_printf/vsprintf-full.o
ppprintf-$(CONFIG_PRINTF_MINI) += $(WRPC_DIR)/pp_printf/vsprintf-mini.o
ppprintf-$(CONFIG_PRINTF_NONE) += $(WRPC_DIR)/pp_printf/vsprintf-none.o
ppprintf-$(CONFIG_PRINTF_XINT) += $(WRPC_DIR)/pp_printf/vsprintf-xint.o

ppprintf-y ?= $(WRPC_DIR)/pp_printf/vsprintf-xint.o

obj-y += $(ppprintf-y)


