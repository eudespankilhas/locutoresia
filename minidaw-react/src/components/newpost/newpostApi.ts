/**
 * API Client for NewPost-IA Integration
 * Handles communication with the backend news automation server
 */

const API_BASE_URL = 'http://localhost:5000';

/**
 * Publishes content to NewPost-IA via backend API
 * @param {Object} data - The post data
 * @param {string} data.content - The post content
 * @param {Array<string>} data.hashtags - Array of hashtags
 * @returns {Promise<Object>} - Result of the publish operation
 */
export const publishToNewPostIA = async (data: { content: string; hashtags: string[] }) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/newpost/publish`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error publishing to NewPost-IA:', error);
    throw error;
  }
};

/**
 * Gets the current status of the news automation
 * @returns {Promise<Object>} - Current automation status
 */
export const getNewsStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news/status`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting news status:', error);
    throw error;
  }
};

/**
 * Starts the news automation
 * @param {Object} options - Options for starting automation
 * @param {Object} options.enabled_sources - Sources to enable
 * @returns {Promise<Object>} - Result of start operation
 */
export const startNewsAutomation = async (options: { enabled_sources: object }) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(options),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error starting news automation:', error);
    throw error;
  }
};

/**
 * Stops the news automation
 * @returns {Promise<Object>} - Result of stop operation
 */
export const stopNewsAutomation = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error stopping news automation:', error);
    throw error;
  }
};

/**
 * Executes a news collection cycle immediately
 * @param {Object} options - Options for execution
 * @param {Object} options.enabled_sources - Sources to use
 * @returns {Promise<Object>} - Result of execution
 */
export const executeNewsCycle = async (options: { enabled_sources: object }) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(options),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error executing news cycle:', error);
    throw error;
  }
};

/**
 * Gets available news sources
 * @returns {Promise<Array>} - List of available sources
 */
export const getNewsSources = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news/sources`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.sources;
  } catch (error) {
    console.error('Error getting news sources:', error);
    throw error;
  }
};

/**
 * Clears the automation logs
 * @returns {Promise<Object>} - Result of clear operation
 */
export const clearNewsLogs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/news/logs/clear`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error clearing news logs:', error);
    throw error;
  }
};

/**
 * Checks if the backend API is healthy
 * @returns {Promise<Object>} - Health status
 */
export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error checking API health:', error);
    throw error;
  }
};
