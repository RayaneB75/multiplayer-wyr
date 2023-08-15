import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

Future<OpenSession> createOpenSession(String name, String password) async {
  final response = await http.post(
    //Uri.parse('http://rayane.space:5000/openSession?JWT_SECRET_KEY=secret'),
    //Uri.parse('http://localhost:48921/openSession?JWT_SECRET_KEY=secret'),
    Uri.parse('http://localhost:5000/openSession?JWT_SECRET_KEY=secret'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: json.encode(<String, String>{
      'name': name,
      'password': password,
    }),
  );

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return OpenSession.fromJson(json.decode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to open session.');
  }
}

class OpenSession {
  final String refreshToken;
  final String token;

  const OpenSession({required this.refreshToken, required this.token});

  factory OpenSession.fromJson(Map<String, dynamic> json) {
    return OpenSession(
      refreshToken: json['refresh_token'],
      token: json['token'],
    );
  }
}

class TestApi extends StatefulWidget {
  const TestApi({super.key});

  @override
  State<TestApi> createState() {
    return _TestApiState();
  }
}

class _TestApiState extends State<TestApi> {
  final TextEditingController _controller = TextEditingController();
  Future<OpenSession>? _futureOpenSession;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Test API',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Test API'),
        ),
        body: Container(
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8),
          child: (_futureOpenSession == null) ? buildColumn() : buildFutureBuilder(),
        ),
      ),
    );
  }

  Column buildColumn() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        TextField(
          controller: _controller,
          decoration: const InputDecoration(hintText: 'Enter login'),
        ),
        ElevatedButton(
          onPressed: () {
            setState(() {
              _futureOpenSession = createOpenSession(_controller.text, "thisIsFront");
            });
          },
          child: const Text('Create Data'),
        ),
      ],
    );
  }

  FutureBuilder<OpenSession> buildFutureBuilder() {
    return FutureBuilder<OpenSession>(
      future: _futureOpenSession,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return Text(snapshot.data!.token);
        } else if (snapshot.hasError) {
          return Text('${snapshot.error}');
        }

        return const CircularProgressIndicator();
      },
    );
  }
}