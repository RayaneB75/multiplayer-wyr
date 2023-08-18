import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiCalls {

  static const String protocol = "http";
  static const String domain = "rayane.space";
  static const String port = "5000";

  static Future<String> openSession() async {
    const String endpoint = "openSession";

    final response = await http.post(
      Uri.parse('$protocol://$domain:$port/$endpoint?JWT_SECRET_KEY=secret'),
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

static Future login(String email, String password, String token) async {
  const String endpoint = "login";

  final response = await http.post(
      Uri.parse('$protocol://$domain:$port/$endpoint'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        HttpHeaders.authorizationHeader: "Bearer $token",
      },
      body: jsonEncode(<String, String>{
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to login');
    }
}

}

