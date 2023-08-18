import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/find_match.dart';

class ApiCalls {
  static String? jwtToken = dotenv.env['JWT_PASSWORD'];
  static String? protocol = dotenv.env['API_SRV_PROTOCOL'];
  static String? domain = dotenv.env['API_SRV_HOSTNAME'];
  static String? port = dotenv.env['API_SRV_PORT'];

  static String token = "";
  static String refreshToken = "";

  static String lastError = "";

  // opensession endpoint management
  static Future openSession() async {
    const String endpoint = "openSession";

    final result = await http.post(
      Uri.parse('$protocol://$domain:$port/$endpoint?JWT_SECRET_KEY=secret'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String?>{
        "name": "front",
        "password": jwtToken,
      }),
    );
    if (result.statusCode == 200) {
      final json = jsonDecode(result.body);

      token = json['token'];
      refreshToken = json['refresh_token'];

    } else {
      throw Exception('Failed to open session');
    }
  }

// login endpoint management
  static Future login(
      String email, String password, BuildContext context) async {
    const String endpoint = "login";
    int result = 0;

    await http
        .post(
          Uri.parse('$protocol://$domain:$port/$endpoint'),
          headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
            HttpHeaders.authorizationHeader: "Bearer $token",
          },
          body: jsonEncode(<String, String>{
            "email": email,
            "password": password,
          }),
        )
        .then((response) => {
              if (response.statusCode == 200)
                {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) =>
                            FindMatchWindow(
                              token: (jsonDecode(response.body))['token'],
                              userId: (jsonDecode(response.body))['user_id'],
                              ),
                      ))
                }
              else
                {
                  showDialog<String>(
                    context: context,
                    builder: (BuildContext context) => AlertDialog(
                      title: const Text('Erreur'),
                      content: Text(jsonDecode(response.body)),
                      actions: <Widget>[
                        TextButton(
                          onPressed: () => Navigator.pop(context, 'OK'),
                          child: const Text('OK'),
                        ),
                      ],
                    ),
                  )
                }
            });

    return result;
  }
}
