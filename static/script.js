new Vue({
    el: '#app',
    data: {
        recognizing: "",    // 音声認識中の内容
        recognized: "",     // 音声認識結果
        summary: "",        // 文字書き起こし内容の要約結果
        startedRecognition: false,  // 音声認識が開始されているかどうか
        recognizer: null,           // 音声認識のインスタンス
        speechServiceToken: null,   // Azure Speech Service の一時利用トークン
        speechServiceRegion: null,  // Azure Speech Service のリージョン
        speechRecognitionLanguage: "ja-JP", // 音声認識の言語
        processing: false,          // 要約処理中かどうか
    },
    mounted() {
        this.setSpeechServiceInfo();
    },
    watch: {
        recognizing: async function () {
            this.summaryzeRecognized();
        },
    },
    methods: {
        // Azure Speech Service の一時利用トークンを取得
        setSpeechServiceInfo: async function () {
            const resp = await axios.get("/api/token");
            this.speechServiceToken = resp.data.token;
            this.speechServiceRegion = resp.data.region;
        },
        // 音声認識の開始・停止
        startRecognition: function () {
            if (this.startedRecognition) {
                this.recognizer.stopContinuousRecognitionAsync();
            } else {
                const speechConfig = SpeechSDK.SpeechConfig.fromAuthorizationToken(this.speechServiceToken, this.speechServiceRegion);
                speechConfig.speechRecognitionLanguage = this.speechRecognitionLanguage;
                const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

                this.recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);
                this.recognizer.recognizing = this.onRecognizing;
                this.recognizer.recognized = this.onRecognized;

                this.recognizer.startContinuousRecognitionAsync();
            }
            this.startedRecognition = !this.startedRecognition;
        },
        // 音声認識のイベントハンドラ
        onRecognizing: async function (sender, e) {
            if (e.result.privText) this.recognizing = e.result.privText;
        },
        // 音声認識結果の処理
        onRecognized: function (sender, e) {
            if (e.privResult.privText) this.recognized += e.privResult.privText;
            this.recognizing = "";
        },
        // 認識結果のクリア
        clearRecognized: async function () {
            this.recognizing = "";
            this.recognized = "";
            this.modifiedText = "";
            this.processing = false;
        },
        // Azure OpenAI Service で認識結果を要約する
        summaryzeRecognized: async function () {
            if (this.processing) return;
            this.processing = true;
            const resp = await axios.post("/api/modify", { text: this.recognized + this.recognizing });
            this.processing = false;
            this.summary = resp.data.summary;
        },
    },
});
