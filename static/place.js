// import { Client } from "@googlemaps/google-maps-services-js";
// import { Language } from "@googlemaps/google-maps-services-js";

// const PLACES_API_APIKEY = ""; //TODO ここにAPIキーを入れる flaskから頑張ってもらってくる
// const client = new Client({});
// const response = await client.placesNearby({ 
//   params: {
//     key: PLACES_API_APIKEY, 
//     language: Language.ja,
//     keyword: "スーパー",
//     location: {lat: 35.6217, lng: 139.7192 },
//     radius: 500,
//   },
// });

// if (response.status !== 200) {
//   // エラー処理
// }

// // response.data.results.length は 最大20件です。
// // response.data.next_page_token を placesNearby({ pagetoken: ... }) に渡すと21件目以降が取得できます 

// console.table(response.data.results.forEach((r) => [r.name, r.vicinity]))



//  ここどうしよう！！！！！！！！(大声)



async function getPlaces(lat, lng, searchWord="スーパー") {
  const apiKey = process.env.GOOGLE_PLACES_API_KEY; // TODO ここにAPIキーを入れる flaskから頑張ってもらってくる
  const radius = 500; // 検索範囲（半径500m）

  // Google Places APIのURL
  let url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${lat},${lng}&radius=${radius}&language=ja&keyword=${encodeURIComponent(
    searchWord
  )}&key=${apiKey}`;

  try {
    const response = await fetch(url); // Google Places APIにリクエストを送信
    const data = await response.json(); // レスポンスのJSONを解析


    // レスポンスデータをクライアントに送信    return data;
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
}