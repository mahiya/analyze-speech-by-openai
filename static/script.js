new Vue({
    el: '#app',
    data: {
        recognizing: "",
        recognized: "",
        systemMessage: "あなたは入力された文章を要約するスペシャリストです。",
        prompt: "音声認識で得た文章を箇条書きで要約してください。",
        processing: false,
        completion: "",
        startedRecognition: false,
        startRecognizeButtonLabel: "音声認識を開始",
        recognizer: null,
        speechServiceToken: null,
        speechServiceRegion: null,
        speechRecognitionLanguage: "ja-JP"
    },
    mounted() {
        this.setSpeechServiceInfo();
    },
    watch: {
        recognizing: async function () {
            this.summaryzeRecognized();
        },
        startedRecognition: async function () {
            this.startRecognizeButtonLabel = this.startedRecognition
                ? "音声認識を停止"
                : "音声認識を開始";
        },
    },
    methods: {
        setSpeechServiceInfo: async function () {
            const resp = await axios.get("/token");
            this.speechServiceToken = resp.data.token;
            this.speechServiceRegion = resp.data.region;
        },
        startRecognition: function () {
            if (this.startedRecognition) {
                this.recognizer.stopContinuousRecognitionAsync();
            } else {
                const speechConfig = SpeechSDK.SpeechConfig.fromAuthorizationToken(
                    this.speechServiceToken,
                    this.speechServiceRegion
                );
                speechConfig.speechRecognitionLanguage = this.speechRecognitionLanguage;
                const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

                this.recognizer = new SpeechSDK.SpeechRecognizer(
                    speechConfig,
                    audioConfig
                );
                this.recognizer.recognizing = this.onRecognizing;
                this.recognizer.recognized = this.onRecognized;

                this.recognizer.startContinuousRecognitionAsync();
            }
            this.startedRecognition = !this.startedRecognition;
        },
        onRecognizing: async function (sender, e) {
            if (e.result.privText) this.recognizing = e.result.privText;
        },
        onRecognized: function (sender, e) {
            if (e.privResult.privText) this.recognized += e.privResult.privText;
            this.recognizing = "";
        },
        clearRecognized: async function () {
            this.recognizing = "";
            this.recognized = "";
            this.completion = "";
            this.processing = false;
        },
        summaryzeRecognized: async function () {
            if (this.processing) return;
            this.processing = true;

            const prompt =
                this.prompt +
                "\n\n#音声認識で得た文章\n" +
                this.recognized +
                this.recognizing;
            const resp = await axios.post("/completion", { prompt });

            this.completion = resp.data.completion;
            this.processing = false;
        },
    },
});
