
import 'package:flutter/material.dart';

class FindMatchWindow extends StatelessWidget {
  const FindMatchWindow({super.key});

  @override
  Widget build(BuildContext context) {
    const appTitle = 'Find Match !';
    return MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true, // material 3 babyyyy
      ),
      title: appTitle,
      home: Scaffold(
        appBar: AppBar(
          title: const Text(appTitle),
        ),
        body: const FindMatchForm(),
      ),
    );
  }
}

class FindMatchForm extends StatelessWidget {
  const FindMatchForm({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: TextFormField(
            decoration: const InputDecoration(
              border: UnderlineInputBorder(),
              labelText: 'Enter player ID',
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: ElevatedButton(
            onPressed: () {
             
            },
            child: const Text('GO !'),
          ),
        ),
      ],
    );
  }
}