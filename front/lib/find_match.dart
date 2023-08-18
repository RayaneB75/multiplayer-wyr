import 'package:flutter/material.dart';
import 'package:frontend/items.dart';

import 'api_calls.dart';

class FindMatchWindow extends StatefulWidget {
  final String token;
  final int userId;

  const FindMatchWindow({super.key, required this.token, required this.userId});

  @override
  State<FindMatchWindow> createState() => _FindMatchWindowState();
}

class _FindMatchWindowState extends State<FindMatchWindow> {
  final _formKey = GlobalKey<FormState>();
  bool _isButtonDisabled = false;
  final idController = TextEditingController();

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed.
    idController.dispose();

    super.dispose();
  }

  Future match(String userId, context) async {
    setState(() {
      _isButtonDisabled = true;
    });
    return await ApiCalls.match(userId, context);
  }

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
        child: Column(children: <Widget>[
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              const Text(
                'Trouve un partenaire !',
                style: TextStyle(fontSize: 30),
              ),
              const SizedBox(height: 120),
              Form(
                key: _formKey,
                child: Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 30, vertical: 16),
                      child: PlayerIDFieldCustom(
                        controller: idController,
                        onChanged: (value) {
                          setState(() {
                            _isButtonDisabled = false;
                          });
                        },
                        content: 'Entrez l\'ID du joueur',
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 16),
                      child: SizedBox(
                        height: 50,
                        width: 150,
                        child: ElevatedButton(
                          onPressed: _isButtonDisabled
                              ? null
                              : () {
                                  bool isFrontValid = false;

                                  if (_formKey.currentState!.validate()) {
                                    isFrontValid = true;
                                  }

                                  if (isFrontValid) {
                                    match(idController.text, context);
                                  }
                                },
                          child: const Text(
                            'Match !',
                            style: TextStyle(
                                fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 8, vertical: 75),
                child: ElevatedButton(
                  onPressed: () {
                    showModalBottomSheet<void>(
                      showDragHandle: true,
                      context: context,
                      builder: (BuildContext context) {
                        return SizedBox(
                          height: 200,
                          child: Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              mainAxisSize: MainAxisSize.min,
                              children: <Widget>[
                                Text('${widget.userId}',
                                    style: const TextStyle(
                                        fontSize: 30,
                                        fontWeight: FontWeight.bold)),
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
          ),
        ]),
      ),
    );
  }
}
