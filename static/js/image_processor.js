class ImageProcessor {
    constructor() {
        this.ctx = null;
    }

    process(imageData, filterType, params) {
        const width = imageData.width;
        const height = imageData.height;
        const data = new Uint8ClampedArray(imageData.data);

        // Ensure params exists
        params = params || {};

        let processed;

        switch (filterType) {
            case 'edge-detection':
                // Canny Edge (Simplified Sobel)
                // params: threshold1 (50), threshold2 (150)
                processed = this.applyCannyEdge(data, width, height, 50, 150);
                break;
            case 'clahe':
                // CLAHE (Simulated)
                // params: clipLimit (2.0)
                processed = this.applyCLAHE(data, width, height, params.claheClipLimit || 2.0);
                break;
            case 'histogram-eq':
                processed = this.applyHistogramEqualization(data, width, height);
                break;
            case 'high-pass':
                processed = this.applyHighPass(data, width, height);
                break;
            case 'gaussian-blur':
                // params: kernelSize (5)
                processed = this.applyGaussianBlur(data, width, height, params.gaussianKernel || 5);
                break;
            case 'median-filter':
                // params: kernelSize (5)
                processed = this.applyMedianFilter(data, width, height, params.medianKernel || 5);
                break;
            case 'wiener-filter':
                // params: noise (0.005)
                processed = this.applyWienerFilter(data, width, height, params.wienerNoise || 0.005);
                break;
            case 'background-subtraction':
                // params: threshold (30)
                processed = this.applyBackgroundSubtraction(data, width, height, params.bgSubThreshold || 30);
                break;
            case 'contrast-stretch':
                // params: min (5), max (95)
                processed = this.applyContrastStretching(data, width, height, params.contrastMin || 5, params.contrastMax || 95);
                break;
            case 'bilateral-filter':
                // params: spatial (5), intensity (30)
                processed = this.applyBilateralFilter(data, width, height, params.bilateralSpatial || 3, params.bilateralIntensity || 30);
                break;
            case 'morphological':
                // params: type ('erode'), kernel (3)
                processed = this.applyMorphological(data, width, height, params.morphType || 'erode', params.morphKernel || 3);
                break;
            case 'thermal':
                processed = this.applyThermal(data, width, height);
                break;
            case 'original':
            default:
                return imageData;
        }

        return new ImageData(processed, width, height);
    }

    // --- Filter Implementations ---

    applyCannyEdge(data, width, height, t1, t2) {
        const output = new Uint8ClampedArray(data.length);
        const gray = this.toGrayscale(data);

        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                const idx = y * width + x;

                // Sobel Kernels
                const gx = -gray[idx - width - 1] - 2 * gray[idx - 1] - gray[idx + width - 1] +
                    gray[idx - width + 1] + 2 * gray[idx + 1] + gray[idx + width + 1];
                const gy = -gray[idx - width - 1] - 2 * gray[idx - width] - gray[idx - width + 1] +
                    gray[idx + width - 1] + 2 * gray[idx + width] + gray[idx + width + 1];

                const mag = Math.sqrt(gx * gx + gy * gy);
                // Green/Cyan edge style
                const val = mag > t1 ? 255 : 0;

                const pIdx = idx * 4;
                output[pIdx] = val;         // R
                output[pIdx + 1] = val > 0 ? 255 : 0; // G
                output[pIdx + 2] = val > 0 ? 255 : 0; // B
                output[pIdx + 3] = 255;
            }
        }
        return output;
    }

    applyCLAHE(data, width, height, clip) {
        // Simple contrast stretch simulation for performance in JS
        const output = new Uint8ClampedArray(data.length);
        for (let i = 0; i < data.length; i += 4) {
            const gray = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
            const val = Math.min(255, Math.pow(gray / 255, 1.1) * 255 * 1.2);
            output[i] = val;
            output[i + 1] = val;
            output[i + 2] = val;
            output[i + 3] = 255;
        }
        return output;
    }

    applyHistogramEqualization(data, width, height) {
        const output = new Uint8ClampedArray(data.length);
        const histogram = new Array(256).fill(0);

        // 1. Calc Histogram
        for (let i = 0; i < data.length; i += 4) {
            const gray = Math.floor(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]);
            histogram[gray]++;
        }

        // 2. Calc CDF
        const cdf = new Array(256);
        cdf[0] = histogram[0];
        for (let i = 1; i < 256; i++) {
            cdf[i] = cdf[i - 1] + histogram[i];
        }

        // 3. Normalize CDF
        const cdfMin = cdf.find(v => v > 0);
        const totalPixels = width * height;
        const lut = cdf.map(v => Math.round(((v - cdfMin) / (totalPixels - cdfMin)) * 255));

        // 4. Apply
        for (let i = 0; i < data.length; i += 4) {
            const gray = Math.floor(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]);
            const newVal = lut[gray];
            output[i] = newVal;
            output[i + 1] = newVal;
            output[i + 2] = newVal;
            output[i + 3] = 255;
        }
        return output;
    }

    applyHighPass(data, width, height) {
        // High pass is often original - blurred, or just edge detection
        // Using Edge logic for simplicity as "High Frequency"
        return this.applyCannyEdge(data, width, height, 30, 100);
    }

    applyGaussianBlur(data, width, height, kernelSize) {
        const output = new Uint8ClampedArray(data.length);
        // Simplified Box Blur for JS performance (Gaussian is heavy in loop)
        const half = Math.floor(kernelSize / 2);

        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                let r = 0, g = 0, b = 0, count = 0;

                for (let ky = -half; ky <= half; ky++) {
                    for (let kx = -half; kx <= half; kx++) {
                        const ny = y + ky;
                        const nx = x + kx;
                        if (ny >= 0 && ny < height && nx >= 0 && nx < width) {
                            const idx = (ny * width + nx) * 4;
                            r += data[idx];
                            g += data[idx + 1];
                            b += data[idx + 2];
                            count++;
                        }
                    }
                }
                const idx = (y * width + x) * 4;
                output[idx] = r / count;
                output[idx + 1] = g / count;
                output[idx + 2] = b / count;
                output[idx + 3] = 255;
            }
        }
        return output;
    }

    applyMedianFilter(data, width, height, kernelSize) {
        const output = new Uint8ClampedArray(data.length);
        const half = Math.floor(kernelSize / 2);

        for (let y = half; y < height - half; y++) {
            for (let x = half; x < width - half; x++) {
                const rVals = [], gVals = [], bVals = [];

                for (let ky = -half; ky <= half; ky++) {
                    for (let kx = -half; kx <= half; kx++) {
                        const idx = ((y + ky) * width + (x + kx)) * 4;
                        rVals.push(data[idx]);
                        gVals.push(data[idx + 1]);
                        bVals.push(data[idx + 2]);
                    }
                }

                rVals.sort((a, b) => a - b);
                gVals.sort((a, b) => a - b);
                bVals.sort((a, b) => a - b);

                const mid = Math.floor(rVals.length / 2);
                const idx = (y * width + x) * 4;
                output[idx] = rVals[mid];
                output[idx + 1] = gVals[mid];
                output[idx + 2] = bVals[mid];
                output[idx + 3] = 255;
            }
        }
        return output;
    }

    applyWienerFilter(data, width, height, noiseVar) {
        // Simplified approximation using local statistics
        const output = new Uint8ClampedArray(data.length);
        const half = 2; // Fixed 5x5 kernel

        for (let y = half; y < height - half; y++) {
            for (let x = half; x < width - half; x++) {
                let rSum = 0, gSum = 0, bSum = 0, count = 0;
                // Local Mean
                for (let ky = -half; ky <= half; ky++) {
                    for (let kx = -half; kx <= half; kx++) {
                        const idx = ((y + ky) * width + (x + kx)) * 4;
                        rSum += data[idx]; gSum += data[idx + 1]; bSum += data[idx + 2];
                        count++;
                    }
                }
                const rMean = rSum / count;
                const gMean = gSum / count;
                const bMean = bSum / count;

                // Local Variance
                let rVar = 0, gVar = 0, bVar = 0;
                for (let ky = -half; ky <= half; ky++) {
                    for (let kx = -half; kx <= half; kx++) {
                        const idx = ((y + ky) * width + (x + kx)) * 4;
                        rVar += (data[idx] - rMean) ** 2;
                        gVar += (data[idx + 1] - gMean) ** 2;
                        bVar += (data[idx + 2] - bMean) ** 2;
                    }
                }
                rVar /= count; gVar /= count; bVar /= count;

                // Filter
                const idx = (y * width + x) * 4;
                const noise = noiseVar * 255 * 255;

                output[idx] = rMean + (Math.max(0, rVar - noise) / Math.max(rVar, 1)) * (data[idx] - rMean);
                output[idx + 1] = gMean + (Math.max(0, gVar - noise) / Math.max(gVar, 1)) * (data[idx + 1] - gMean);
                output[idx + 2] = bMean + (Math.max(0, bVar - noise) / Math.max(bVar, 1)) * (data[idx + 2] - bMean);
                output[idx + 3] = 255;
            }
        }
        return output;
    }

    applyBackgroundSubtraction(data, width, height, threshold) {
        const output = new Uint8ClampedArray(data.length);
        // Estimate "background" as simple average of current frame (naïve) 
        // Ideally needs previous frames, but for single frame logic we check deviation from global mean

        let rSum = 0, gSum = 0, bSum = 0;
        for (let i = 0; i < data.length; i += 4) { rSum += data[i]; gSum += data[i + 1]; bSum += data[i + 2]; }
        const rAvg = rSum / (width * height);
        const gAvg = gSum / (width * height);
        const bAvg = bSum / (width * height);

        for (let i = 0; i < data.length; i += 4) {
            const rDiff = Math.abs(data[i] - rAvg);
            const gDiff = Math.abs(data[i + 1] - gAvg);
            const bDiff = Math.abs(data[i + 2] - bAvg);

            if (rDiff > threshold || gDiff > threshold || bDiff > threshold) {
                output[i] = data[i]; output[i + 1] = data[i + 1]; output[i + 2] = data[i + 2];
            } else {
                output[i] = 0; output[i + 1] = 0; output[i + 2] = 0;
            }
            output[i + 3] = 255;
        }
        return output;
    }

    applyContrastStretching(data, width, height, minP, maxP) {
        // Simple Min-Max stretch 
        const output = new Uint8ClampedArray(data.length);
        let min = 255, max = 0;

        // Find min/max luminance
        for (let i = 0; i < data.length; i += 4) {
            const gray = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
            if (gray < min) min = gray;
            if (gray > max) max = gray;
        }

        for (let i = 0; i < data.length; i += 4) {
            for (let j = 0; j < 3; j++) {
                output[i + j] = ((data[i + j] - min) / (max - min || 1)) * 255;
            }
            output[i + 3] = 255;
        }
        return output;
    }

    applyBilateralFilter(data, width, height, sigmaS, sigmaI) {
        // Expensive in JS, doing a very lightweight approximation (smart blur)
        // Check edges -> keep, flat -> blur
        return this.applyGaussianBlur(data, width, height, 3); // Fallback for now due to complexity
    }

    applyMorphological(data, width, height, type, kernel) {
        // Erode / Dilate
        const output = new Uint8ClampedArray(data.length);
        const half = Math.floor(kernel / 2);
        const gray = this.toGrayscale(data);
        const isDilate = (type === 'dilate' || type === 'close');

        for (let y = half; y < height - half; y++) {
            for (let x = half; x < width - half; x++) {
                let val = isDilate ? 0 : 255;

                for (let ky = -half; ky <= half; ky++) {
                    for (let kx = -half; kx <= half; kx++) {
                        const idx = (y + ky) * width + (x + kx);
                        const v = gray[idx];
                        if (isDilate) val = Math.max(val, v);
                        else val = Math.min(val, v);
                    }
                }

                const idx = (y * width + x) * 4;
                output[idx] = output[idx + 1] = output[idx + 2] = val;
                output[idx + 3] = 255;
            }
        }
        return output;
    }

    applyThermal(data, width, height) {
        const output = new Uint8ClampedArray(data.length);
        for (let i = 0; i < data.length; i += 4) {
            const gray = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
            let r = 0, g = 0, b = 0;
            if (gray < 128) {
                b = 255; g = gray * 2;
            } else {
                b = (255 - gray) * 2; g = 255; r = (gray - 128) * 2;
            }
            output[i] = r; output[i + 1] = g; output[i + 2] = b; output[i + 3] = 255;
        }
        return output;
    }

    toGrayscale(data) {
        const gray = new Uint8ClampedArray(data.length / 4);
        for (let i = 0; i < data.length; i += 4) {
            gray[i / 4] = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
        }
        return gray;
    }
}

window.ImageProcessor = ImageProcessor;
