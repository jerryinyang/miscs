//
//  ed.c
//  DTAIDistanceC
//
//  Created by Wannes Meert on 13/07/2020.
//  Copyright © 2020 Wannes Meert. All rights reserved.
//

#include "dd_ed.h"



{% set use_ndim = 0 %}
{% set inner_dist = 'squaredeuclidean' %}
{%- include 'ed_distance.jinja.c' %}


{% set use_ndim = 0 %}
{% set inner_dist = 'euclidean' %}
{%- include 'ed_distance.jinja.c' %}


{% set use_ndim = 1 %}
{% set inner_dist = 'squaredeuclidean' %}
{%- include 'ed_distance.jinja.c' %}


{% set use_ndim = 1 %}
{% set inner_dist = 'euclidean' %}
{%- include 'ed_distance.jinja.c' %}

