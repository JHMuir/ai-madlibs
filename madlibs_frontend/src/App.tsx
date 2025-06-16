import React, { useState } from 'react';
import { Sparkles, Image, Loader2, Wand2, BookOpen, RefreshCw } from 'lucide-react';

interface MadLibsTemplate {
  template_id: string;
  template: string;
  word_types: string[];
  topic: string;
}

interface CompletedMadLib {
  madlib_id: string;
  completed_text: string;
  comic_prompt: string;
  panel_suggestions: string;
}

// API configuration
const API_URL = 'http://localhost:8000';

const MadLibsApp: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [template, setTemplate] = useState<MadLibsTemplate | null>(null);
  const [userInputs, setUserInputs] = useState<{ [key: string]: string }>({});
  const [completedMadLib, setCompletedMadLib] = useState<CompletedMadLib | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingImage, setLoadingImage] = useState(false);
  const [currentStep, setCurrentStep] = useState<'topic' | 'filling' | 'completed'>('topic');

  const generateTemplate = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/generate-template`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });
      const data = await response.json();
      setTemplate(data);
      setCurrentStep('filling');

      // Initialize user inputs
      const inputs: { [key: string]: string } = {};
      data.word_types.forEach((wordType: string) => {
        inputs[wordType] = '';
      });
      setUserInputs(inputs);
    } catch (error) {
      console.error('Error generating template:', error);
      alert('Failed to generate template. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const submitMadLib = async () => {
    if (!template) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/submit-madlib`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          template_id: template.template_id,
          user_inputs: userInputs,
        }),
      });
      const data = await response.json();
      setCompletedMadLib(data);
      setCurrentStep('completed');
    } catch (error) {
      console.error('Error submitting madlib:', error);
      alert('Failed to submit MadLib. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateImage = async () => {
    if (!completedMadLib) return;

    setLoadingImage(true);
    try {
      const response = await fetch(`${API_URL}/api/generate-image`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          madlib_id: completedMadLib.madlib_id,
        }),
      });
      const data = await response.json();
      setImageUrl(`${API_URL}${data.image_url}`);
    } catch (error) {
      console.error('Error generating image:', error);
      alert('Failed to generate image. Please try again.');
    } finally {
      setLoadingImage(false);
    }
  };

  const startOver = () => {
    setTopic('');
    setTemplate(null);
    setUserInputs({});
    setCompletedMadLib(null);
    setImageUrl(null);
    setCurrentStep('topic');
  };

  const isFormComplete = () => {
    return Object.values(userInputs).every(value => value.trim() !== '');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-6xl font-bold text-white mb-2 drop-shadow-lg flex items-center justify-center gap-3">
            MadLibs Generator
          </h1>
          <p className="text-xl text-white/90 drop-shadow">Create stories with your imagination!</p>
        </div>

        {/* Main Content Card */}
        <div className="bg-white/95 backdrop-blur rounded-3xl shadow-2xl p-8 transform transition-all duration-300 hover:scale-[1.02]">

          {/* Step 1: Topic Selection */}
          {currentStep === 'topic' && (
            <div className="space-y-6 animate-fadeIn">
              <div className="text-center">
                <BookOpen className="w-16 h-16 mx-auto text-purple-600 mb-4" />
                <h2 className="text-3xl font-bold text-gray-800 mb-2">What's Your Story About?</h2>
                <p className="text-gray-600">Pick any topic you like!</p>
              </div>

              <div className="max-w-md mx-auto">
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter your topic here!"
                  className="w-full px-6 py-4 text-lg border-3 border-purple-300 rounded-2xl focus:outline-none focus:border-purple-500 transition-colors placeholder:text-center"
                  onKeyPress={(e) => e.key === 'Enter' && topic && generateTemplate()}
                />

                <button
                  onClick={generateTemplate}
                  disabled={!topic || loading}
                  className="w-full mt-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-4 px-8 rounded-2xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-105 flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" />
                      Creating Your Story...
                    </>
                  ) : (
                    <>
                      <Wand2 />
                      Create MadLib Template
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Fill in the Blanks */}
          {currentStep === 'filling' && template && (
            <div className="space-y-6 animate-fadeIn">
              <div className="text-center">
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Fill in the Blanks!</h2>
                <p className="text-gray-600">Add your silly words to complete the story</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto pr-2">
                {template.word_types.map((wordType, index) => (
                  <div key={index} className="transform transition-all duration-200">
                    <label className="block text-sm font-bold text-purple-700 mb-1 capitalize">
                      {wordType}
                    </label>
                    <input
                      type="text"
                      value={userInputs[wordType] || ''}
                      onChange={(e) => setUserInputs({ ...userInputs, [wordType]: e.target.value })}
                      placeholder={`Enter a ${wordType}`}
                      className="w-full px-4 py-3 border-2 border-purple-300 rounded-xl focus:outline-none focus:border-purple-500 transition-colors"
                    />
                  </div>
                ))}
              </div>

              <div className="flex gap-4 justify-center">
                <button
                  onClick={startOver}
                  className="bg-gray-500 text-white font-bold py-3 px-6 rounded-xl hover:bg-gray-600 transition-colors flex items-center gap-2"
                >
                  <RefreshCw className="w-5 h-5" />
                  Start Over
                </button>
                <button
                  onClick={submitMadLib}
                  disabled={!isFormComplete() || loading}
                  className="bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold py-3 px-8 rounded-xl hover:from-green-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-105 flex items-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" />
                      Creating Story...
                    </>
                  ) : (
                    <>
                      <Sparkles />
                      Complete MadLib!
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Completed Story */}
          {currentStep === 'completed' && completedMadLib && (
            <div className="space-y-6 animate-fadeIn">
              <div className="text-center">
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Your Silly Story!</h2>
              </div>

              <div className="bg-purple-50 p-6 rounded-2xl border-2 border-purple-200">
                <p className="text-lg leading-relaxed text-gray-800 whitespace-pre-wrap">
                  {completedMadLib.completed_text}
                </p>
              </div>

              {!imageUrl && (
                <div className="text-center">
                  <button
                    onClick={generateImage}
                    disabled={loadingImage}
                    className="bg-gradient-to-r from-blue-500 to-cyan-600 text-white font-bold py-4 px-8 rounded-2xl hover:from-blue-600 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-105 flex items-center gap-2 mx-auto"
                  >
                    {loadingImage ? (
                      <>
                        <Loader2 className="animate-spin" />
                        Drawing Your Story...
                      </>
                    ) : (
                      <>
                        <Image />
                        Generate Comic Image
                      </>
                    )}
                  </button>
                </div>
              )}

              {imageUrl && (
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-center text-gray-800">Your Story as a Picture!</h3>
                  <div className="rounded-2xl overflow-hidden shadow-xl">
                    <img
                      src={imageUrl}
                      alt="Generated MadLib illustration"
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              )}

              <div className="text-center">
                <button
                  onClick={startOver}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-3 px-8 rounded-2xl hover:from-purple-700 hover:to-pink-700 transform transition-all duration-200 hover:scale-105 flex items-center gap-2 mx-auto"
                >
                  <RefreshCw />
                  Create Another Story!
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MadLibsApp;
