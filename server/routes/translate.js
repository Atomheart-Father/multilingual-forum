const express = require('express');
const axios = require('axios');
const router = express.Router();

// Translation service selector
class TranslationService {
  constructor() {
    this.services = {
      openai: this.translateWithOpenAI.bind(this),
      azure: this.translateWithAzure.bind(this),
      google: this.translateWithGoogle.bind(this),
      deepl: this.translateWithDeepL.bind(this)
    };
  }

  async translateWithOpenAI(text, targetLang, sourceLang = 'auto') {
    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'system',
              content: `You are a professional translator. Translate the following text to ${targetLang}. Maintain the original tone and context. Only return the translated text, no explanations.`
            },
            {
              role: 'user',
              content: text
            }
          ],
          max_tokens: 1000,
          temperature: 0.3
        },
        {
          headers: {
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        translatedText: response.data.choices[0].message.content.trim(),
        service: 'openai',
        detectedLanguage: 'unknown' // OpenAI doesn't provide detection
      };
    } catch (error) {
      throw new Error(`OpenAI translation failed: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  async translateWithAzure(text, targetLang, sourceLang = 'auto') {
    try {
      const endpoint = 'https://api.cognitive.microsofttranslator.com/translate';
      const params = {
        'api-version': '3.0',
        'to': targetLang
      };
      
      if (sourceLang !== 'auto') {
        params.from = sourceLang;
      }

      const response = await axios.post(
        endpoint,
        [{ text }],
        {
          headers: {
            'Ocp-Apim-Subscription-Key': process.env.AZURE_TRANSLATE_KEY,
            'Ocp-Apim-Subscription-Region': process.env.AZURE_TRANSLATE_REGION,
            'Content-Type': 'application/json'
          },
          params
        }
      );

      const result = response.data[0];
      return {
        translatedText: result.translations[0].text,
        service: 'azure',
        detectedLanguage: result.detectedLanguage?.language || 'unknown'
      };
    } catch (error) {
      throw new Error(`Azure translation failed: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  async translateWithGoogle(text, targetLang, sourceLang = 'auto') {
    try {
      const response = await axios.post(
        'https://translation.googleapis.com/language/translate/v2',
        {
          q: text,
          target: targetLang,
          source: sourceLang === 'auto' ? undefined : sourceLang
        },
        {
          headers: {
            'Content-Type': 'application/json'
          },
          params: {
            key: process.env.GOOGLE_TRANSLATE_KEY
          }
        }
      );

      const result = response.data.data.translations[0];
      return {
        translatedText: result.translatedText,
        service: 'google',
        detectedLanguage: result.detectedSourceLanguage || 'unknown'
      };
    } catch (error) {
      throw new Error(`Google translation failed: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  async translateWithDeepL(text, targetLang, sourceLang = 'auto') {
    try {
      const response = await axios.post(
        'https://api-free.deepl.com/v2/translate',
        {
          text: [text],
          target_lang: targetLang.toUpperCase(),
          source_lang: sourceLang === 'auto' ? undefined : sourceLang.toUpperCase()
        },
        {
          headers: {
            'Authorization': `DeepL-Auth-Key ${process.env.DEEPL_API_KEY}`,
            'Content-Type': 'application/json'
          }
        }
      );

      const result = response.data.translations[0];
      return {
        translatedText: result.text,
        service: 'deepl',
        detectedLanguage: result.detected_source_language?.toLowerCase() || 'unknown'
      };
    } catch (error) {
      throw new Error(`DeepL translation failed: ${error.response?.data?.message || error.message}`);
    }
  }

  async translate(text, targetLang, sourceLang = 'auto', preferredService = 'openai') {
    const service = this.services[preferredService];
    if (!service) {
      throw new Error(`Unsupported translation service: ${preferredService}`);
    }

    try {
      return await service(text, targetLang, sourceLang);
    } catch (error) {
      console.error(`Primary service ${preferredService} failed:`, error.message);
      
      // Fallback to other services
      const fallbackServices = Object.keys(this.services).filter(s => s !== preferredService);
      
      for (const fallbackService of fallbackServices) {
        try {
          console.log(`Trying fallback service: ${fallbackService}`);
          return await this.services[fallbackService](text, targetLang, sourceLang);
        } catch (fallbackError) {
          console.error(`Fallback service ${fallbackService} failed:`, fallbackError.message);
        }
      }
      
      throw new Error('All translation services failed');
    }
  }
}

const translationService = new TranslationService();

// POST /api/translate
router.post('/', async (req, res) => {
  try {
    const { text, targetLang, sourceLang = 'auto', service = 'openai' } = req.body;

    if (!text || !targetLang) {
      return res.status(400).json({
        error: 'Missing required parameters: text and targetLang'
      });
    }

    if (text.length > 5000) {
      return res.status(400).json({
        error: 'Text too long. Maximum 5000 characters allowed.'
      });
    }

    const result = await translationService.translate(text, targetLang, sourceLang, service);
    
    res.json(result);
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({
      error: 'Translation failed',
      message: error.message
    });
  }
});

// GET /api/translate/languages
router.get('/languages', (req, res) => {
  const supportedLanguages = {
    'zh': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'pl': 'Polish',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'tr': 'Turkish',
    'el': 'Greek',
    'he': 'Hebrew',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'id': 'Indonesian',
    'ms': 'Malay',
    'tl': 'Filipino',
    'uk': 'Ukrainian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'sr': 'Serbian',
    'sl': 'Slovenian',
    'sk': 'Slovak',
    'ro': 'Romanian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian'
  };

  res.json(supportedLanguages);
});

module.exports = router; 