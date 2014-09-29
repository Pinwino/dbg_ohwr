/* This work is part of the White Rabbit project
 * 
 * Jose Jimenez  <jjimenez.wr@gmail.com>, Copyright (C) 2014 UGR.
 *
 * Released according to the GNU GPL version 3 (GPLv3) or later.
 * 
 */


#include <linux/math64.h>
#include <linux/time.h>
#include <kernel2lm32_layer.h>

unsigned long msecs_to_jiffies(const unsigned int m){
	return m*20*1000;
}

unsigned int jiffies_to_msecs(const unsigned long j){
	return  div_u64_rem(j, 20*1000, NULL);
}

void getnstimeofday (struct timespec *ts){
	pr_err("function: %s not implmented yet!", __func__);
}
