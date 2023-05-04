import React from "react";
import { Unity, useUnityContext } from "react-unity-webgl";

export default function Unity1() {
    const { unityProvider } = useUnityContext({
        loaderUrl: "build/build.loader.js",
        dataUrl: "build/build.data",
        frameworkUrl: "build/build.framework.js",
        codeUrl: 'build/build.wasm',
    });

    return <Unity unityProvider={unityProvider} />;
}

// https://react-unity-webgl.dev/