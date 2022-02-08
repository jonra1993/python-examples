import os
from deepspeech import Model
from scipy.io import wavfile
import time
import glob


def timer():
    return time.time()
    


"""
Load the pre-trained model into the memory
@param models: Output Graph Protocol Buffer file
@param scorer: Scorer file
 
@Retval
Returns a list [DeepSpeech Object, Model Load Time, Scorer Load Time]
"""


def load_model(models, scorer):
    model_load_start = timer()
    ds: Model = Model(models)
    model_load_end = timer() - model_load_start
    print("Loaded model in %0.3fs." % (model_load_end))

    scorer_load_start = timer()
    ds.enableExternalScorer(scorer)
    scorer_load_end = timer() - scorer_load_start
    print("Loaded external scorer in %0.3fs." % (scorer_load_end))

    return [ds, model_load_end, scorer_load_end]


"""
Resolve directory path for the models and fetch each of them.
@param dir_name: Path to the directory containing pre-trained models
 
@Retval:
Retunns a tuple containing each of the model files (pb, scorer)
"""


def resolve_models(dir_name):
    pb = glob.glob(dir_name + "/*.pbmm")[0]
    print("Found Model: %s" % pb)

    scorer = glob.glob(dir_name + "/*.scorer")[0]
    print("Found scorer: %s" % scorer)

    return pb, scorer


"""
Run Inference on input audio file
@param ds: Deepspeech object
@param audio: Input audio for running inference on
@param fs: Sample rate of the input audio file
 
@Retval:
Returns a list [Inference, Inference Time, Audio Length]
 
"""


def stt(ds, audio, fs):
    inference_time = 0.0
    audio_length = len(audio) * (1 / fs)

    # Run Deepspeech
    print("Running inference...")
    inference_start = timer()
    output = ds.stt(audio)
    inference_end = timer() - inference_start
    inference_time += inference_end
    print(
        "Inference took %0.3fs for %0.3fs audio file." % (inference_end, audio_length)
    )

    return [output, inference_time]


def main():
    # need audio, aggressive, and model
    # Point to a path containing the pre-trained models & resolve ~ if used
    folder = "./models/v0.9.3/"
    dir_name = os.path.expanduser(folder)

    # Resolve all the paths of model files
    output_graph, scorer = resolve_models(dir_name)
    print("{} and {}".format(output_graph, scorer))

    # Load output_graph, alphabet and scorer
    model_retval = load_model(output_graph, scorer)

    title_names = [
        "Filename",
        "Duration(s)",
        "Inference Time(s)",
        "Model Load Time(s)",
        "Scorer Load Time(s)",
    ]
    print(
        "\n%-30s %-20s %-20s %-20s %s"
        % (
            title_names[0],
            title_names[1],
            title_names[2],
            title_names[3],
            title_names[4],
        )
    )

    wave_file = "./audio/2830-3980-0043.wav"
    sample_rate, data = wavfile.read(wave_file)

    output = stt(model_retval[0], data, sample_rate)
    print("Transcript: %s" % output[0])


if __name__ == "__main__":
    main()
