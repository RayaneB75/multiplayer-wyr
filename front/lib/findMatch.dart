
import 'package:flutter/material.dart';

class FindMatchWindow extends StatelessWidget {
  const FindMatchWindow({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Find Match !'),
      ),
      body: const Center(
        child: FindMatchForm()
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