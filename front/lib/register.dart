import 'package:flutter/material.dart';
import 'package:frontend/findMatch.dart';
import 'package:frontend/items.dart';

class RegisterWindow extends StatelessWidget {
  const RegisterWindow({super.key});

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
      body: const Center(
        child: RegisterForm()
      ),
    );
  }
}

class RegisterForm extends StatelessWidget {
  const RegisterForm({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: <Widget>[

        const Text(
          'S\'enregistrer',
          style: TextStyle(fontSize: 30),
        ),

        const SizedBox(height: 120),

        const TextFieldCustom(content: "Entre ton e-mail IMT Atlantique"),
        const TextFieldCustom(content: "Entre ton mot de passe"),
        const TextFieldCustom(content: "Confirme ton mot de passe"),

        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: ElevatedButton(
            onPressed: () {
             Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const FindMatchWindow()),
                );
            },
            child: const Text('S\'enregistrer'),
          ),
        ),
      ],
    );
  }
}