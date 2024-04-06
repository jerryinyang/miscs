
/*!
 Keogh lower bound for DTW.
 */
{%- if "euclidean" == inner_dist %}
{%- set suffix="_euclidean" %}
{%- else %}
{%- set suffix="" %}
{%- endif %}
seq_t lb_keogh{{ suffix }}(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, DTWSettings *settings) {
    {%- if inner_dist != "euclidean" %}
    if (settings->inner_dist == 1) {
        return lb_keogh_euclidean(s1, l1, s2, l2, settings);
    }
    {%- endif %}
    idx_t window = settings->window;
    if (window == 0) {
        window = MAX(l1, l2);
    }
    idx_t imin, imax;
    seq_t t = 0;
    seq_t ui;
    seq_t li;
    seq_t ci;
    idx_t imin_diff = window - 1;
    if (l1 > l2) {
        imin_diff += l1 - l2;
    }
    idx_t imax_diff = window;
    if (l2 > l1) {
        imax_diff += l2 - l1;
    }
    for (idx_t i=0; i<l1; i++) {
        if (i > imin_diff) {
            imin = i - imin_diff;
        } else {
            imin = 0;
        }
        imax = i + imax_diff;
        if (imax > l2) {
            imax = l2;
        }
        ui = 0;
        for (idx_t j=imin; j<imax; j++) {
            if (s2[j] > ui) {
                ui = s2[j];
            }
        }
        li = INFINITY;
        for (idx_t j=imin; j<imax; j++) {
            if (s2[j] < li) {
                li = s2[j];
            }
        }
        ci = s1[i];
        if (ci > ui) {
            {%- if inner_dist == "squaredeuclidean" %}
            t += (ci - ui)*(ci - ui);
            {%- else %}
            t += fabs(ci - ui);
            {%- endif %}
        } else if (ci < li) {
            {%- if inner_dist == "squaredeuclidean" %}
            t += (li - ci)*(li - ci);
            {%- else %}
            t += li - ci;
            {%- endif %}
        }
    }
    {%- if inner_dist == "squaredeuclidean" %}
    t = sqrt(t);
    {%- endif %}
    return t;
}
