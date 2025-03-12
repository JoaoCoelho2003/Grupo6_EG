# TPC4

```
SA(start) { soma:int}
SA(elems) { soma:int, ok:bool}
SA(elem)  { val:int, ok:bool}


start : "("  elems  ")"
ER	{
          start.soma = elems.soma;
}
TR	{ 
          print( start.soma );
}

elems  : elem
ER{ 
    elems.soma = elem.val if elem.ok else 0 ;
    elems.ok = elem.ok; 
}

TR  { print(elems[1].ok); }

|  elems  "," elem
ER { 
     elems[1].soma = elems[2].soma + (elem.val if elems[2].ok else 0);
     elems[1].ok = elems[2].ok and elem.ok;
}
TR {  print(elem.ok); }

elem :
NUM
ER	{ elem.val = int(NUM);
	  elem.ok = True;
 }
|  PAL
ER	{ elem.val = 0;
          elem.ok = (True if (PAL == "inicio") else False);
}

NUM : /-?\d+/
PAL  : /\b(inicio|fim)\b/
```

### Casos do contador

(inicio, 1, 2, fim) -> 3

(inicio, 1, inicio, 2, fim) -> 3

(inicio, 1, fim,inicio, 2, fim) -> 1

(inicio, 1,inicio,3,4,5,6, fim,inicio 2,6,7, fim,3) -> 19


###### Ver alternativa (opcional)

(inicio, 1, inicio,3 ,fim ,2 ,3, fim,3) -> 8

