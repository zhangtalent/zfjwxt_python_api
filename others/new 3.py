def b64tohex(s) {
  ret = ""
  k = 0; 
  # b64 state, 0-3
  for(i = 0; i < s.length; ++i) {
    if(s.charAt(i) == b64pad) 
		break;
    v = b64map.indexOf(s.charAt(i));
    if(v < 0) 
		continue;
    if(k == 0) {
      ret += int2char(v >> 2);
      slop = v & 3;
      k = 1;
    }
    else if(k == 1) {
      ret += int2char((slop << 2) | (v >> 4));
      slop = v & 0xf;
      k = 2;
    }
    else if(k == 2) {
      ret += int2char(slop);
      ret += int2char(v >> 2);
      slop = v & 3;
      k = 3;
    }
    else {
      ret += int2char((slop << 2) | (v >> 4));
      ret += int2char(v & 0xf);
      k = 0;
    }
  }
  if(k == 1)
    ret += int2char(slop << 2);
  return ret;
}