/*!
Euclidean distance between two sequences of values, can differ in length.

If the two series differ in length, compare the last element of the shortest series
to the remaining elements in the longer series. This is compatible with Euclidean
distance being used as an upper bound for DTW.
 
{%- if use_ndim == 1 %}
The sequences represent a sequence of n-dimensional vectors. The array is
assumed to be c-contiguous with as 1st dimension the sequence and the
2nd dimension the n-dimensional vector.
{%- endif %}

@param s1 : Sequence of numbers.
@param s2 : Sequence of numbers.
@return Euclidean distance
*/
{%- if use_ndim == 0 %}
{%- set suffix = "" %}
{%- else %}
{%- set suffix = "_ndim" %}
{%- endif %}
{%- if inner_dist == "euclidean" %}
{%- set suffix = suffix + "_euclidean" %}
{%- else %}
{%- set suffix = suffix + "" %}
{%- endif %}
seq_t euclidean_distance{{ suffix }}(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2{% if use_ndim == 1 %}, int ndim{% endif %}) {
    idx_t n = MIN(l1, l2);
    {%- if use_ndim == 1 %}
    idx_t idx;
    seq_t d;
    {%- endif %}
    seq_t ub = 0;
    for (idx_t i=0; i<n; i++) {
        {%- if use_ndim == 0 %}
        {%- if inner_dist == "euclidean" %}
        ub += fabs(s1[i] - s2[i]);
        {%- else %}
        ub += SEDIST(s1[i], s2[i]);
        {%- endif %}
        {%- else %}
        idx = i*ndim;
        d = 0;
        for (int d=0; d<ndim; d++) {
            d += SEDIST(s1[idx + d], s2[idx + d]);
        }
        {%- if inner_dist == "euclidean" %}
        d = sqrt(d);
        {%- endif %}
        ub += d;
        {%- endif %}
    }
    // If the two series differ in length, compare the last element of the shortest series
    // to the remaining elements in the longer series
    if (l1 > l2) {
        for (idx_t i=n; i<l1; i++) {
            {%- if use_ndim == 0 %}
            {%- if inner_dist == "euclidean" %}
            ub += fabs(s1[i] - s2[n-1]);
            {%- else %}
            ub += SEDIST(s1[i], s2[n-1]);
            {%- endif %}
            {%- else %}
            idx = i*ndim;
            d = 0;
            for (int d=0; d<ndim; d++) {
                d += SEDIST(s1[idx + d], s2[(n-1)*ndim]);
            }
            {%- if inner_dist == "euclidean" %}
            d = sqrt(d);
            {%- endif %}
            ub += d;
            {%- endif %}
        }
    } else if (l1 < l2) {
        for (idx_t i=n; i<l2; i++) {
            {%- if use_ndim == 0 %}
            {%- if inner_dist == "euclidean" %}
            ub += fabs(s1[n-1] - s2[i]);
            {%- else %}
            ub += SEDIST(s1[n-1], s2[i]);
            {%- endif %}
            {%- else %}
            idx = i*ndim;
            d = 0;
            for (int d=0; d<ndim; d++) {
                d += SEDIST(s1[(n-1)*ndim], s2[idx + d]);
            }
            {%- if inner_dist == "euclidean" %}
            d = sqrt(d);
            {%- endif %}
            ub += d;
            {%- endif %}
        }
    }
    {%- if inner_dist == "squaredeuclidean" %}
    ub = sqrt(ub);
    {%- endif %}
    return ub;
}
