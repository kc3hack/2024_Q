// 地図を表示するためのグローバル変数
let map;
let marker;
let count = 0;
function initMap() {
  // 地図のオプションを設定
  const mapOptions = {
    zoom: 14, // ズームレベル
    center: { lat: 34.651, lng: 135.586 }, // 地図の中心点（デフォルトの位置）
  };

  // 地図を表示
  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  marker = new google.maps.Marker({
    position: { lat: 34.651, lng: 135.586 },
    title: "Hello World!",
  });
}

function displayPlaces() {
  marker.setMap(null);
  count = 0;
  navigator.geolocation.getCurrentPosition(getPlaces, fail);
}

function fail(error) {
  window.alert("位置情報の取得に失敗しました。エラーコード：" + error.code);
}

// レスポンスデータをもとにDOMを構築
// 店舗一覧を出すならここ
function displayDataOnPage(data, position) {
  const placesContainer = document.getElementById("places");
  // 検索結果をクリア
  placesContainer.innerHTML = "";

  // Google Places APIのレスポンスデータをもとにDOMを構築
  data.results.forEach((place) => {
    const placeElement = document.createElement("div");
    placeElement.classList.add("place");
    const nameElement = document.createElement("p");
    nameElement.textContent = count + ". " + place.name + " ";
    placeElement.appendChild(nameElement);

    if (place.vicinity) {
      const addressElement = document.createElement("p");
      addressElement.textContent = `住所: ${place.vicinity}`;
      placeElement.appendChild(addressElement);
    }

    const distance = document.createElement("p");
    distance.textContent =
      "距離: " +
      Math.round(
        calculateDistance(
          position.coords.latitude,
          position.coords.longitude,
          place.geometry.location.lat,
          place.geometry.location.lng
        ) * 100
      ) /
        100 +
      "km";
    placeElement.appendChild(distance);
    const mapLatLng = new google.maps.LatLng(
      place.geometry.location.lat,
      place.geometry.location.lng
    );
    new google.maps.Marker({
      map: map, // 対象の地図オブジェクト
      position: mapLatLng, // 緯度・経度
      label: String(count),
    });

    const mapLink = document.createElement("a");
    mapLink.href = `https://www.google.com/maps/search/?api=1&query=${place.name}`;
    mapLink.textContent = "Google Mapsで見る";
    mapLink.target = "_blank";
    placeElement.appendChild(mapLink);

    placesContainer.appendChild(placeElement);
    count++;
  });
}

function displayMarker(lat, lng) {
    marker = new google.maps.Marker({
        position: { lat: lat, lng: lng },
        map: map,
    });
    marker.setMap(map); //ちょっとわからん
}


function getPlaces(position) {
  // positionを引数として追加
  const lat = position.coords.latitude;
  const lng = position.coords.longitude;
  // 地図の中心をユーザーの現在位置に更新
  const userLocation = new google.maps.LatLng(lat, lng);
  map.setCenter(userLocation);

//   "hospitalType"パラメータの値を取得
//   const urlParams = new URLSearchParams(window.location.search);
//   const hospitalType = urlParams.get("hospitalType");
//   let text = document.getElementById("midasi");
//   if (hospitalType) {
//     text.innerText = hospitalType + "について検索しました";
//     getPlacesFromBackend(lat, lng, hospitalType, position);
//   }

  new google.maps.Marker({
    map: map, // 対象の地図オブジェクト
    position: { lat: lat, lng: lng },
  });
}


// バックエンドからデータを取得 -> displayDataOnPageを呼び出す
// 今したいことはテーブルからデータを取得して表示すること
function getPlacesFromBackend(lat, lng, hospitalType, position) {
  fetch("http://localhost:3000/get-places", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      lat: lat,
      lng: lng,
      hospitalType: hospitalType,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      displayDataOnPage(data, position);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// 2点間の距離を計算
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // 地球の半径(km)
  const rad = Math.PI / 180;
  const dLat = (lat2 - lat1) * rad;
  const dLon = (lon2 - lon1) * rad;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * rad) *
      Math.cos(lat2 * rad) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c; // 距離 (km)
  return distance;
}


