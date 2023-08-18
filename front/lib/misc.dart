import 'dart:convert';

String getToken(String json) {
  return jsonDecode(json)['token'];
}
