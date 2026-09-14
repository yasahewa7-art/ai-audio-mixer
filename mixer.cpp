#include <iostream>
#include <vector>
#include <sndfile.h>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: ./mixer <input1.wav> <input2.wav> <output.wav>\n";
        return 1;
    }

    std::string file1 = argv[1];
    std::string file2 = argv[2];
    std::string outfile = argv[3];

    SF_INFO sfinfo1, sfinfo2;
    SNDFILE *snd1 = sf_open(file1.c_str(), SFM_READ, &sfinfo1);
    SNDFILE *snd2 = sf_open(file2.c_str(), SFM_READ, &sfinfo2);

    if (!snd1 || !snd2) {
        std::cerr << "Error opening input audio files!\n";
        return 1;
    }

    // Read samples (simplified mono/stereo buffer handling)
    std::vector<float> buf1(sfinfo1.frames * sfinfo1.channels);
    std::vector<float> buf2(sfinfo2.frames * sfinfo2.channels);

    sf_readf_float(snd1, buf1.data(), sfinfo1.frames);
    sf_readf_float(snd2, buf2.data(), sfinfo2.frames);

    // Mixing logic (combining buffers safely)
    size_t min_frames = std::min(sfinfo1.frames, sfinfo2.frames);
    std::vector<float> mixed(min_frames * sfinfo1.channels);

    for (size_t i = 0; i < mixed.size(); ++i) {
        mixed[i] = (buf1[i] * 0.6f) + (buf2[i] * 0.6f); // Balanced mixing
    }

    // Save output
    SF_INFO out_info = sfinfo1;
    out_info.frames = min_frames;
    SNDFILE *out = sf_open(outfile.c_str(), SFM_WRITE, &out_info);
    sf_writef_float(out, mixed.data(), min_frames);

    sf_close(snd1);
    sf_close(snd2);
    sf_close(out);

    std::cout << "C++ Mixing Completed Successfully!\n";
    return 0;
}
