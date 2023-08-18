import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

class ApiCalls {

  static const String protocol = "https";
  static String? domain = dotenv.env['API_SRV_HOSTNAME'];
  static String? port = dotenv.env['API_SRV_PORT'];

  static String token = "";
  static String refreshToken= "";

  static String lastError ="";

  // opensession endpoint management
  static Future openSession() async {
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

      token = json['token'];
      refreshToken = json['refresh_token'];

    } else {
      throw Exception('Failed to open session');
    }

}

// login endpoint management
static Future login(String email, String password) async {
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
      return 200;
    } else {
      setLastError(jsonDecode(response.body));
      return 400;
      //throw Exception(jsonDecode(response.body));
    }
}

static String getLastError() {
  return lastError;
}

static void setLastError(String err) {
  lastError = err;
}

}

