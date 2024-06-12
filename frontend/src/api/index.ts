import { Status } from "../interfaces";

// const baseUrl = "http://localhost:5000";
const baseUrl = "https://jukesites.com/apis/rpc";

export const useFetch = async (url: string) => {
  let isError = undefined;
  let isLoading = false;
  let fetchData: any | Status = undefined;

  try {
    isLoading = true;
    const response = await fetch(baseUrl + url);
    const responseData = await response.json();
    fetchData = responseData;
    isLoading = false;
  } catch (e: Error | unknown) {
    isError = e instanceof Error ? e.message : "Error fetching data";
  } finally {
    isLoading = false;
  }

  if (url === "/status")
    return { isError, data: fetchData as Status, isLoading };
  return { isError, data: fetchData, isLoading };
};

export const usePost = async (url: string, data: any) => {
  let isError = undefined;
  let isLoading = false;
  let postData: any = [];

  try {
    isLoading = true;
    const response = await fetch(baseUrl + url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseData = await response.json();
    postData = responseData;
    isLoading = false;
  } catch (e: Error | unknown) {
    isError = e instanceof Error ? e.message : "Error fetching data";
  } finally {
    isLoading = false;
  }

  return { isError, data: postData, isLoading };
};
