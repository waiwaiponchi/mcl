import sys

def gen_func(name, ret, args, cname, params, i):
	retstr = '' if ret == 'void' else ' return'
	print(f'extern "C" {ret} {cname}{i}({args});')
	print(f'template<> {ret} {name}<{i}>({args}) {{{retstr} {cname}{i}({params}); }}')

def gen_switch(name, ret, args, cname, params, n):
	ret0 = 'return' if ret == 'void' else 'return 0'
	print(f'''inline {ret} {name}({args}, size_t n)
{{
	switch (n) {{
	default: assert(0); {ret0};''')
	for i in range(1, n):
		if i == 8:
			print('#if MCL_SIZEOF_UNIT == 4')
		call = f'{cname}<{i}>({params})'
		if ret == 'void':
			print(f'\tcase {i}: {call}; return;')
		else:
			print(f'\tcase {i}: return {call};')
	print('#endif\n\t}\n}')


arg_p3 = 'Unit *z, const Unit *x, const Unit *y'
arg_p2u = 'Unit *z, const Unit *x, Unit y'
param_u3 = 'z, x, y'

N = 16

if len(sys.argv) != 2:
	print('python3 src/gen_bitint_header.py (asm|switch)')
	sys.exit(1)

arg = sys.argv[1]

if arg == 'asm':
	print('// this code is generated by python3 src/gen_bitint_header.py', arg)

	for i in range(1, N+1):
		if i == 8:
			print('#if MCL_SIZEOF_UNIT == 4')
		gen_func('addT', 'Unit', arg_p3, 'mclb_add', param_u3, i)
		gen_func('subT', 'Unit', arg_p3, 'mclb_sub', param_u3, i)
		gen_func('mulUnitT', 'Unit', arg_p2u, 'mclb_mulUnit', param_u3, i)
		gen_func('mulUnitAddT', 'Unit', arg_p2u, 'mclb_mulUnitAdd', param_u3, i)
	print('#endif')

elif arg == 'switch':
	print('// this code is generated by python3 src/gen_bitint_header.py', arg)
	gen_switch('addN', 'Unit', arg_p3, 'addT', param_u3, N)
	gen_switch('subN', 'Unit', arg_p3, 'subT', param_u3, N)
	gen_switch('mulUnit', 'Unit', arg_p2u, 'mulUnitT', param_u3, N)
	gen_switch('mulUnitAdd', 'Unit', arg_p2u, 'mulUnitAddT', param_u3, N)
	gen_switch('mul', 'void', arg_p3, 'mulT', param_u3, N)

else:
	print('err', arg)

