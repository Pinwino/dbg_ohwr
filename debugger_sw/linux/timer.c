/* This work is part of the White Rabbit project
 * 
 * Jose Jimenez  <jjimenez.wr@gmail.com>, Copyright (C) 2014 UGR.
 *
 * Released according to the GNU GPL version 3 (GPLv3) or later.
 * 
 */


#include "stdlib.h"
#include "hw/irq_timer.h"
#include <linux/timer.h>
#include <linux/jiffies.h>
#include <dbg.h>


extern unsigned char * BASE_TIMER;
extern int fd_calib_period_s;

int setup_timer(struct timer_list *timer, void (*function)(unsigned long),
															unsigned long data)
{
	timer->function = function;	
	timer->data=data;
	return 0;
}

int mod_timer(struct timer_list *timer, unsigned long long expires)
{
	timer->expires=fd_calib_period_s*0x3B9ACA0;
	/* due to time ambiguity */
	irq_timer_writel(&timer->itmr, 0x0, TIMER_SEL);
	if(timer->expires != timer->itmr.timer_dead_line 
				|| !irq_timer_check_armed(&timer->itmr)) 
	{
		timer->itmr.timer_dead_line = timer->expires;
		irq_timer_set_time(&timer->itmr, timer->itmr.timer_dead_line);
	}
	if(!irq_timer_check_armed(&timer->itmr))
	{
		irq_timer_sel_cascade(&timer->itmr, cascade_disable);
		irq_timer_time_mode(&timer->itmr, diff_time_periodic);
		irq_timer_arm(&timer->itmr, timer_arm);
	}
	return 0;
}
