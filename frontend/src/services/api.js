import axios from 'axios';

const API_URL = process.env.VUE_APP_API_BASE_URL;

export const getProducts = async () => {
  try {
    const response = await axios.get(`${API_URL}/product/list/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar produtos:", error);
    throw error;
  }
};

export const getProductDetail = async (sku) => {
  try {
    const response = await axios.get(`${API_URL}/product/detail/${sku}/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes do produto:", error);
    throw error;
  }
};

export const getProductsByCategory = async (categoryName) => {
  const response = await axios.get(`${API_URL}/product/list/?category=${encodeURIComponent(categoryName)}`);
  return response.data;
};

export const getCategoryById = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/category/detail/${id}/`); 
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar a categoria com ID ${id}:`, error);
    throw error; 
  }
};

export const getSupplierById = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/supplier/detail/${id}/`); 
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar o fornecedor com ID ${id}:`, error);
    throw error; 
  }
};

export const getCategories = async () => {
  try {
    const response = await axios.get(`${API_URL}/category/list/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar categorias:", error);
    throw error;
  }
};

export const getStockBySku = async (sku) => {
  try {
    const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/stock/detail/${sku}/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar quantidade em estoque:", error);
    throw error;
  }
};

export const fetchPaymentTypes = async () => {
  try {
    const response = await axios.get(`${API_URL}/payment-types/list/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar tipos de pagamento:", error);
    throw error;
  }
};