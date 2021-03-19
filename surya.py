from decrypt import two, one

a2 = two(7, 2)
a1 = one(6, 1)
b1 = one(a1.create_object_two().do_stuff_inline(),
         a2.one_cha_object.do_stuff_inline()).do_stuff(9, 10)
print(b1)
