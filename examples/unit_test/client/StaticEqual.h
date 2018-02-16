/*
 * Copyright (c) 2006-2017 by
 * Visual Technology Services Ltd.
 * All Rights Reserved
 *
 * This software comprises unpublished confidential information
 * including intellectual property of Visual Technology Services Ltd.
 * and may not be used, copied or made available to anyone, except in
 * accordance with the licence under which it is furnished.
 *
 */

#ifndef VTSL_STATIC_EQUAL_COPY_SEMANTIC
#define VTSL_STATIC_EQUAL_COPY_SEMANTIC
#include <cstring>

template <class T>
inline bool builtin_equal(T first, T second)
{
    return first == second;
}

template <class T, class U>
inline bool builtin_equal(T first, U second)
{
    return first == second;
}

inline bool builtin_equal(const char* first, const char* second)
{
    return strcmp(first, second) == 0;
}

#endif /* VTSL_STATIC_EQUAL_COPY_SEMANTIC */
