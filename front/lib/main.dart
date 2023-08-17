import 'package:flutter/material.dart';
import 'package:frontend/api_calls.dart';
import 'package:frontend/register.dart';
import 'package:frontend/login.dart';

void main() {
  runApp( MaterialApp(
    title: 'Tu préfère by ResEl',
    home: const Home(),
    theme: ThemeData.light(
        useMaterial3: true,
        ),
  ));
}

class Home extends StatelessWidget {
  const Home({super.key});

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
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              'Tu préfère ...',
              style: TextStyle(fontSize: 30),
            ),
            const SizedBox(height: 120),
            ElevatedButton(
              child: const Text('Enregistrement'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const RegisterWindow()),
                );
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              child: const Text('Connexion'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginWindow()),
                );
              },
            ),
            const SizedBox(height: 100),
            ElevatedButton(
              child: const Text('TEST API'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const TestApi()),
                );
              },
            ),
          ],
        ),
        
      ),
    );
  }
}