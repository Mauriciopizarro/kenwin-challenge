name = "access_token"
value = "example"

var curCookie = name + "=" + value +
    ", expires=" + ATS_getExpire() +
    ", path=" + path +
    ", domain=" + domain;

document.cookie = curCookie;