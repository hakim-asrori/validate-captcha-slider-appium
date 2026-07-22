import { remote } from "webdriverio";

const driver = await remote({
  protocol: "http",
  hostname: "127.0.0.1",
  port: 4723,
  path: "/",
  connectionRetryCount: 3,
  connectionRetryTimeout: 45000,
  logLevel: "error",
  capabilities: {
    platformName: "Android",
    "appium:deviceName": "0611625123009007",
    "appium:automationName": "UiAutomator2",
    "appium:noReset": true,
    "appium:fullReset": false,
    "appium:appPackage": "com.android.chrome",
    "appium:appActivity": "com.google.android.apps.chrome.Main",
    "appium:ensureWebviewsHavePages": false,
    "appium:autoGrantPermissions": true,
    "appium:appWaitActivity": "*",
    "appium:appWaitDuration": 5000,
    "appium:newCommandTimeout": 0, // Never timeout (0 = infinite)
    "appium:uiautomator2ServerInstallTimeout": 120000,
    "appium:adbExecTimeout": 120000,
    "appium:connectHardwareKeyboard": true,
    "appium:uiautomator2ServerLaunchTimeout": 60000,
    "appium:uiautomator2ServerReadTimeout": 120000,
    "appium:orientation": "PORTRAIT",
    "appium:autoWebview": false,
    "appium:disableWindowAnimation": true,
    "appium:ignoreHiddenApiPolicyError": true,
    "appium:skipDeviceInitialization": false,
    "appium:skipServerInstallation": false,
    "appium:udid": "0611625123009007",
  },
});

async function main() {
  await driver.url("http://10.255.10.137:5173/");
  await driver.pause(5000);

  driver.saveScreenshot("screenshot.png");

  const formData = new FormData();
  const base64 = await driver.takeScreenshot();
  const buffer = Buffer.from(base64, "base64");
  formData.append(
    "file",
    new Blob([buffer], { type: "image/png" }),
    "screenshot.png",
  );
  await driver.pause(4000);

  try {
    const response = await fetch("http://127.0.0.1:8800/detect", {
      method: "POST",
      body: formData,
    });
    const data: any = await response.json();
    console.log(data);

    const gapCenter = data.gap_center;
    const confidence = data.confidence;

    await driver.pause(10000);
    const sliderButtonElm = driver.$(
      `//android.widget.Button[@content-desc="Geser untuk menyelesaikan captcha"]`,
    );

    const sliderLocation = await sliderButtonElm.getLocation();
    const sliderSize = await sliderButtonElm.getSize();
    const startX = sliderLocation.x + sliderSize.width / 2;
    const startY = sliderLocation.y + sliderSize.height / 2;

    await driver.pause(2000);
    const captchaLocation = await driver
      .$(
        `/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout`,
      )
      .getLocation();
    const absoluteGapX = captchaLocation.x + gapCenter.x;

    const distanceX = absoluteGapX - startX;
    console.log(`Jarak geser: ${distanceX}px`);

    const steps = Math.floor(Math.random() * 10) + 15; // 15-25 steps

    let currentX = 0;
    const actions: any = [
      {
        type: "pointer",
        id: "finger1",
        parameters: { pointerType: "touch" },
        actions: [],
      },
    ];

    const pointerActions = actions[0]?.actions;
    pointerActions.push({
      type: "pointerMove",
      duration: 0,
      x: startX,
      y: startY,
    });
    pointerActions.push({ type: "pointerDown", button: 0 });
    pointerActions.push({ type: "pause", duration: 50 });

    for (let i = 0; i < steps; i++) {
      const progress = (i + 1) / steps;
      const easedProgress = 1 - Math.pow(1 - progress, 2); // ease-out quadratic
      const targetX = distanceX * easedProgress;
      const stepX = targetX - currentX;
      const jitterY = Math.random() * 4 - 2; // -2 sampai 2

      pointerActions.push({
        type: "pointerMove",
        duration: Math.floor(Math.random() * 30) + 10,
        origin: "pointer",
        x: Math.round(stepX),
        y: Math.round(jitterY),
      });

      currentX = targetX;
    }

    // overshoot lalu koreksi (perilaku manusia)
    const overshoot = Math.random() * 4 + 2;
    pointerActions.push({
      type: "pointerMove",
      duration: 30,
      origin: "pointer",
      x: Math.round(overshoot),
      y: 0,
    });
    pointerActions.push({ type: "pause", duration: 50 });
    pointerActions.push({
      type: "pointerMove",
      duration: 30,
      origin: "pointer",
      x: Math.round(-overshoot),
      y: 0,
    });

    pointerActions.push({
      type: "pause",
      duration: Math.floor(Math.random() * 200) + 100,
    });
    pointerActions.push({ type: "pointerUp", button: 0 });

    await driver.performActions(actions);
    await driver.releaseActions();
  } catch (error) {}

  await driver.pause(20000);
  await driver.deleteSession();
}

main();
