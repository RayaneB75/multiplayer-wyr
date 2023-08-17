import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future openSession() async {
  final response = await http.post(
    Uri.parse('http://rayane.space:5000/openSession?JWT_SECRET_KEY=secret'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      "name": "front",
      "password": "thisIsFront",
    }),
  );

  if (response.statusCode == 200) {
    final json = jsonDecode(response.body);
    return json['token'];
  } else {
    throw Exception('Failed to open session');
  }

}