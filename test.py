def validate(c_v):
    a_c = 1
    code = 1111
    a_c -= 1
    if is_correct := code == c_v:
        ...
    elif not a_c:
        ...
    else:
        raise
    return is_correct

print(validate(111))
