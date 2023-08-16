
import 'package:flutter/material.dart';
import 'package:frontend/wyr.dart';

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
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: TextFormField(
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Enter player ID',
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: ElevatedButton(
            onPressed: () {
             Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const CardExampleApp()),
                );
            },
            child: const Text('GO !'),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: ElevatedButton(
            onPressed: () {
                showModalBottomSheet<void>(
                context: context,
                builder: (BuildContext context) {
                  return const SizedBox(
                    height: 200,
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget>[
                        Text('Player ID'),
                          // ElevatedButton(
                          //   child: const Text('Close BottomSheet'),
                          //   onPressed: () => Navigator.pop(context),
                          // ),
                        ],
                      ),
                    ),
                  );
                },
              );
            },
            child: const Text('Show player ID'),
          ),
        ),
      ],
    );
  }
}