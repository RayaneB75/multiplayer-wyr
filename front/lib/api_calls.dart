import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:frontend/login.dart';
import 'package:frontend/wyr.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/find_match.dart';

class ApiCalls {
  static const String protocol =
      String.fromEnvironment('API_SRV_PROTOCOL', defaultValue: 'http');
  static const String domain =
      String.fromEnvironment('API_SRV_HOSTNAME', defaultValue: 'localhost');
  static const String port =
      String.fromEnvironment('API_SRV_PORT', defaultValue: '5000');

  static String token = "";
  static String refreshToken = "";

  static String loginToken = "";

  static int userId = 0;

  // opensession endpoint management
  static Future openSession() async {
    const String endpoint = "openSession";

    final result = await http.post(
      Uri.parse('$protocol://$domain:$port/$endpoint'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String?>{
        "name": "front",
        "password": const String.fromEnvironment('FRONT_TOKEN'),
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
                  Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => FindMatchWindow(
                          token: loginToken =
                              (jsonDecode(response.body))['token'],
                          userId: userId =
                              (jsonDecode(response.body))['user_id'],
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

  // match endpoint management
  static Future match(String userId, BuildContext context) async {
    const String endpoint = "match";
    int result = 0;

    await http
        .post(
          Uri.parse('$protocol://$domain:$port/$endpoint'),
          headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
            HttpHeaders.authorizationHeader: "Bearer $loginToken",
          },
          body: jsonEncode(<String, String>{
            "userId": userId,
          }),
        )
        .then((response) => {
              if (response.statusCode == 200)
                {
                  pullQuestions(
                      context, (jsonDecode(response.body))['dueled_user']),
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

  // match endpoint management
  static Future pullQuestions(BuildContext context, String playedUser) async {
    const String endpoint = "pull";
    int result = 0;

    await http.get(
      Uri.parse('$protocol://$domain:$port/$endpoint'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        HttpHeaders.authorizationHeader: "Bearer $loginToken",
      },
    ).then((response) => {
          if (response.statusCode == 200)
            {
              Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => WyrWindow(
                      firstProp: (jsonDecode(response.body))['first_prop'],
                      secondProp: (jsonDecode(response.body))['second_prop'],
                      userId: userId,
                      playedUser: playedUser,
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

  // match endpoint management
  static Future pushAnswer(BuildContext context) async {
    const String endpoint = "push";
    int result = 0;

    await http.get(
      Uri.parse('$protocol://$domain:$port/$endpoint'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        HttpHeaders.authorizationHeader: "Bearer $loginToken",
      },
      // body: jsonEncode(<String, int>{
      //   "userId": userId,
      // }),
    ).then((response) => {
          if (response.statusCode == 200)
            {
              Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => FindMatchWindow(
                      token: loginToken,
                      userId: userId,
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

  static Future register(
      String email, String password, BuildContext context) async {
    const String endpoint = "register";
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
                  Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const LoginWindow(),
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
