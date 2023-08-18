import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:universal_html/html.dart' as html;

import 'package:flutter/material.dart';
import 'package:frontend/api_calls.dart';
import 'package:frontend/register.dart';
import 'package:frontend/login.dart';

void main() async {
  runApp(const Main());

  final splash = html.querySelector('#splash');
  if (splash != null) {
    await loadEnv();
    await ApiCalls.openSession();
    splash.remove();
  }
}

Future<void> loadEnv() async {
  await dotenv.load(fileName: ".env");
}

class Main extends StatelessWidget {
  const Main({super.key});

  // Check if the user is connected, if not,
  // redirect to the login page

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tu préfères ? by ResEl',
      home: const MainPage(),
      theme: ThemeData.light(
        useMaterial3: true,
      ),
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {

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
                  MaterialPageRoute(
                      builder: (context) => const RegisterWindow()),
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
          ],
        ),
      ),
    );
  }
}
