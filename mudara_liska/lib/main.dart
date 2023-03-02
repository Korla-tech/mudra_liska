import 'package:bitsdojo_window/bitsdojo_window.dart';
import 'package:flutter/material.dart';
import 'package:mudara_liska/home_page.dart';
import 'package:tray_manager/tray_manager.dart';
import 'package:macos_ui/macos_ui.dart';

const appDimensions = Size(320, 480);

String input = "";
String output = "";

void main() {
  runApp(const MyApp());

  doWhenWindowReady(() {
    trayManager.setIcon('images/tray_icon_inactive.png').then((noValue) {
      var listener = TrayClickListener();
      trayManager.addListener(listener);
      if (true) {
        listener.onTrayIconMouseUp();
      }
    });
  });
}

class TrayClickListener extends TrayListener {
  @override
  Future<void> onTrayIconMouseUp() async {
    if (appWindow.isVisible) {
      trayManager.setIcon('images/tray_icon_inactive.png').then((noValue) {
        appWindow.minimize();
      });
    } else {
      trayManager
          .setIcon('images/tray_icon_active.png')
          .then((noValue) => trayManager.getBounds())
          .then((rect) {
        appWindow.minSize = appDimensions;
        appWindow.maxSize = appDimensions;
        appWindow.size = appDimensions;
        if (rect != null) {
          var x = rect.left > rect.top ? rect.left : rect.top;
          var y = x == rect.left ? rect.top : rect.left;
          appWindow.position = Offset(x - (appDimensions.width / 2), y + 4);
          appWindow.title = 'mudra liška';
          appWindow.show();
        }
      });
    }
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MacosApp(
        theme: MacosThemeData.light(),
        darkTheme: MacosThemeData.dark(),
        themeMode: ThemeMode.system,
        debugShowCheckedModeBanner: false,
        home: const HomePage());
  }
}
