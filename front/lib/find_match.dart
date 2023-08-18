import 'package:flutter/material.dart';
import 'package:frontend/wyr.dart';

class FindMatchWindow extends StatelessWidget {
  final String? token;
  final int userId;
  
  const FindMatchWindow({super.key, required this.token, required this.userId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Image.asset(
          'assets/logo_resel.png',
          fit: BoxFit.contain,
          height: 32,
        ),
      ),
      body: Center(
        child: Column(
          children:<Widget>[
            FindMatchForm(userId: userId),
            // more if necessary 
          ]
        )
      ),
    );
  }
}

class FindMatchForm extends StatefulWidget {
  final int userId;

  const FindMatchForm({super.key, required this.userId});

  @override
  State<FindMatchForm> createState() => _FindMatchFormState();

}

class _FindMatchFormState extends State<FindMatchForm> {

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: <Widget>[
        const Text(
          'Trouve un partenaire !',
          style: TextStyle(fontSize: 30),
        ),
        const SizedBox(height: 120),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 16),
          child: TextFormField(
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Entre l\'identifiant du joueur',
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: SizedBox(
            height: 50,
            width: 150,
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const WyrWindow()),
                );
              },
              child: const Text(
                'Match !',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 75),
          child: ElevatedButton(
            onPressed: () {
              showModalBottomSheet<void>(
                context: context,
                builder: (BuildContext context) {
                  return SizedBox(
                    height: 200,
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget>[
                         Text('$widget.userId'),
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
            child: const Text('Mon identifiant'),
          ),
        ),
      ],
    );
  }
}
