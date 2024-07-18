import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:ui/core/utils/cognito_service.dart';
import 'package:ui/presentation/screens/home.dart';
import 'package:ui/presentation/screens/login_page.dart';

void main() async {
  await dotenv.load(fileName: '.env');
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});
  final authService = AuthService();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Veggie Gourmet',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(fontFamily: 'NotoSansJP'),
      home: FutureBuilder(
        future: authService.isLoggedIn(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            if (snapshot.data == true) {
              return Home();
            } else {
              return LoginPage();
            }
          } else {
            return const Scaffold(
                body: Center(child: CircularProgressIndicator()));
          }
        },
      ),
    );
  }
}
